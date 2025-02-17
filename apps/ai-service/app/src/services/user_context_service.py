from __future__ import annotations

from http import HTTPStatus
from typing import Any, Dict, NamedTuple

import requests
from aws_lambda_powertools import Logger

from src.common.config import Config
from src.common.phi_access_level import PhiAccessLevel
from src.exceptions.central_api_exceptions import (
    BadResponse,
    CentralApiCommunicationFailed,
)
from src.models.tokens.tokens import DecodedAwsIdTokenTypeDef, VerifiedTokens
from src.models.user_context.user_claims_context import UserClaimsContext
from src.models.user_context.user_claims_context_builder import UserClaimsContextBuilder
from src.models.user_context.user_context import UserContextTypeDef
from src.models.user_context.user_context_builder import UserContextBuilder
from src.services.user_service import UserService


class UserIdentifiers(NamedTuple):
    account_uuid: str
    organization_uuid: str


class UserContextService:
    _user_service: UserService
    logger: Logger

    def __init__(
        self,
        user_service: UserService,
        logger: Logger = Logger(),
        config: Config = Config(),
    ) -> None:
        self._user_service = user_service
        self.config = config
        self.logger = logger

    def _get_user_identifiers(
        self,
        cookie: str,
        username: str,
        issuer: str,
    ) -> UserIdentifiers:
        """
        Attempts to retrieve a User's accountUuid and organizationUuid from
        cache. if not present, it will attempt to retrieve it from Central-API.

        Args:
            username(str): The username of the to retrieve from cache
            cookie(str): The cookie that was sent with the request.

        Returns:
            Tuple(str,str): Tuple of account_uuid and organization_uuid
        """
        self.logger.info("Retrieving User Identifiers")
        cognito_user_pool_id = issuer.split("/")[-1]
        user_identifiers = self._get_user_from_cache(
            username,
            cognito_user_pool_id,
        )

        if user_identifiers:
            return user_identifiers

        return self._get_user_information_from_central_api(
            cognito_user_pool_id=cognito_user_pool_id,
            cookie=cookie,
            username=username,
        )

    def _get_user_from_cache(
        self,
        username: str,
        cognito_user_pool_id: str,
    ) -> UserIdentifiers | None:
        user_item = self._user_service.get_user_by_username(
            username,
            cognito_user_pool_id,
        )

        if not user_item:
            return None

        return UserIdentifiers(
            str(user_item.account_uuid),
            str(user_item.organization_uuid),
        )

    def _get_user_information_from_central_api(
        self,
        cookie: str,
        username: str,
        cognito_user_pool_id: str,
    ) -> UserIdentifiers:
        """
        Retrieves a Dictionary that describes a user from Central-API, and
            return their accountUuid as a string.

        Returns:
            Tuple(str,str): Tuple of account_uuid and organization_uuid

        Raises:
            CentralApiCommunicationFailed: When Central-API return anything
                other than 200/Ok response.

            BadAccountUuid: When Central-API's response does not include an
                account_uuid attribute or organization_uuid attribute.
        """
        self.logger.info("Requesting User Information From Central-API")
        response = requests.get(
            f"{self.config.CENTRAL_API_ENDPOINT}/auth/user",
            headers={
                "Cookie": cookie,
            },
        )
        self.logger.info("Making Request")
        if response.status_code != HTTPStatus.OK:
            self.logger.info(
                "central-api says",
                extra={
                    "status_code": response.status_code,
                    "response": response.json(),
                },
            )
            raise CentralApiCommunicationFailed(
                status_code=response.status_code,
            )

        data: Dict[str, Any] = response.json()
        account_uuid = data.get("accountUuid")
        organization_uuid = data.get("organization", {}).get("uuid")

        if not account_uuid or not organization_uuid:
            raise BadResponse

        self.logger.info(
            "Retrieved User",
            extra={
                "account_uuid": account_uuid,
                "organization_uuid": organization_uuid,
            },
        )
        self.logger.info("Caching User")
        self._user_service.create_user(
            account_uuid=account_uuid,
            cognito_user_pool_id=cognito_user_pool_id,
            organization_uuid=organization_uuid,
            username=username,
        )

        return UserIdentifiers(
            account_uuid,
            organization_uuid,
        )

    def _get_claims_from_verified_id_token(
        self,
        verified_id_token: DecodedAwsIdTokenTypeDef,
    ) -> UserClaimsContext:
        """
        Accepts a verified and decoded ID token and creates an object that
        represents a User's claims.

        Args:
            verified_id_token(DecodedAwsIdToken): Decoded ID token with custom
                claims.

        Returns:
            UserClaimsContext
        """

        return (
            UserClaimsContextBuilder()
            .build_query(verified_id_token.get("custom:build_query", False))
            .can_share(verified_id_token.get("custom:can_share", False))
            .irb_memberships(verified_id_token.get("custom:irb_memberships", ""))
            .phi_access_level(
                verified_id_token.get("custom:phi_access_level", PhiAccessLevel.NONE)
            )
            .validate_data(verified_id_token.get("custom:validate_data", False))
            .download_data(verified_id_token.get("custom:download_data", False))
            .version_view(verified_id_token.get("custom:version_view", False))
            .build()
        )

    def user_context_from_verified_tokens(
        self,
        verified_tokens: VerifiedTokens,
        cookie: str,
    ) -> UserContextTypeDef:
        """
        Returns a UserContext - a representation of a User making requests of
        an API Gateway that an Authorizer is protecting.
        """
        user_identifiers = self._get_user_identifiers(
            cookie=cookie,
            username=verified_tokens.id_token["cognito:username"],
            issuer=verified_tokens.id_token["iss"],
        )
        claims = self._get_claims_from_verified_id_token(verified_tokens.id_token)

        self.logger.info("Building Context")

        return (
            UserContextBuilder()
            .account_uuid(user_identifiers.account_uuid)
            .cookie(cookie)
            .email(verified_tokens.id_token["email"])
            .first_name(verified_tokens.id_token["given_name"])
            .last_name(verified_tokens.id_token["family_name"])
            .organization_uuid(user_identifiers.organization_uuid)
            .role(verified_tokens.id_token.get("custom:role", ""))
            .user_claims(claims)
            .username(verified_tokens.id_token["cognito:username"])
            .build_context()
        )

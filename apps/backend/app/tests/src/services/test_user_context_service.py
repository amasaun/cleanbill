import os
from http import HTTPStatus
from typing import Callable, Optional, Tuple

import boto3
import pytest
from pytest_mock import MockerFixture
from requests_mock.adapter import _Matcher
from requests_mock.mocker import Mocker

from src.exceptions.central_api_exceptions import CentralApiCommunicationFailed
from src.models.dynamo.user import UserItem
from src.models.tokens.tokens import VerifiedTokens
from src.models.user_context.user_claims_context import UserClaimsContext
from src.models.user_context.user_context import UserContext
from src.repositories.user_repository import UserRepository
from src.services.user_context_service import UserContextService
from src.services.user_service import UserService
from src.type_defs.decoded_jwts import DecodedAwsIdTokenTypeDef

user_service = UserService(
    UserRepository(
        boto3.resource("dynamodb").Table(
            os.environ["IDP_TABLE"],
        )
    )
)
user_context_service = UserContextService(user_service)


class TestUserContextService:
    class TestGetUserInformationFromCentralApi:
        def test_gets_account_and_org_uuid_from_central_api(
            self,
            central_api_auth_user_mock: Tuple[str, str, _Matcher],
        ) -> None:
            account_uuid, organization_uuid, mock = central_api_auth_user_mock

            retrieved_identifiers = (
                user_context_service._get_user_information_from_central_api(
                    username="",
                    cookie="",
                    cognito_user_pool_id="",
                )
            )

            assert mock.called_once
            assert retrieved_identifiers.account_uuid == account_uuid
            assert retrieved_identifiers.organization_uuid == organization_uuid

        @pytest.mark.parametrize(
            "status_code",
            [
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.FORBIDDEN,
            ],
        )
        def test_should_raise_central_api_communication_failed(
            self,
            status_code: HTTPStatus,
            central_api_auth_user_status_mock: Callable[
                [HTTPStatus, Optional[str]],
                Mocker,
            ],
        ) -> None:
            mock = central_api_auth_user_status_mock(status_code, "")

            with pytest.raises(CentralApiCommunicationFailed):
                user_context_service._get_user_information_from_central_api(
                    username="",
                    cookie="",
                    cognito_user_pool_id="",
                )

                assert mock.called_once

        def test_should_cache_user(
            self,
            central_api_auth_user_mock: Tuple[str, str, _Matcher],
            mocker: MockerFixture,
        ) -> None:
            username = "test"
            cognito_user_pool_id = "us-east-1_someTestPoolId"
            spy = mocker.spy(
                user_service,
                "create_user",
            )

            identifiers = user_context_service._get_user_information_from_central_api(
                username=username,
                cookie="",
                cognito_user_pool_id=cognito_user_pool_id,
            )

            spy.assert_called_once_with(
                identifiers.account_uuid,
                identifiers.organization_uuid,
                username,
                cognito_user_pool_id,
            )

    class TestGetClaimsFromVerifiedIdTokens:
        def test_should_build_expected_user_claims_context(
            self,
            decoded_aws_id_token: DecodedAwsIdTokenTypeDef,
            user_claims_context: UserClaimsContext,
        ) -> None:
            built_user_claims_context = (
                user_context_service._get_claims_from_verified_id_token(
                    decoded_aws_id_token
                )
            )

            assert built_user_claims_context == user_claims_context

    class TestUserContextFromVerifiedTokens:
        def test_should_build_expected_user_context(
            self,
            aws_access_token: str,
            central_api_auth_user_mock: Tuple[str, str, _Matcher],
            decoded_aws_id_token: DecodedAwsIdTokenTypeDef,
            user_context_callable: Callable[[str, str, str], UserContext],
        ) -> None:
            (
                account_uuid_as_str,
                organization_uuid_as_str,
                _,
            ) = central_api_auth_user_mock
            cookie = ""
            expected_context = user_context_callable(
                account_uuid_as_str,
                organization_uuid_as_str,
                cookie,
            )

            built_user_context = user_context_service.user_context_from_verified_tokens(
                cookie=cookie,
                verified_tokens=VerifiedTokens(
                    access_token=aws_access_token,
                    id_token=decoded_aws_id_token,
                ),
            )

            assert built_user_context == expected_context.context()

    class TestGetUserFromCache:
        def test_retrieves_user_from_cache(
            self,
            persisted_user: UserItem,
        ) -> None:
            identifiers = user_context_service._get_user_from_cache(
                persisted_user.username,
                persisted_user.cognito_user_pool_id,
            )

            assert identifiers is not None
            assert (
                str(persisted_user.account_uuid),
                str(persisted_user.organization_uuid),
            ) == identifiers

    def test_should_return_none(self) -> None:
        identifiers = user_context_service._get_user_from_cache(
            username="",
            cognito_user_pool_id="",
        )

        assert identifiers is None

    class TestGetIdentifiers:
        def test_should_get_from_cache(
            self,
            central_api_auth_user_mock: Tuple[str, str, _Matcher],
            persisted_user: UserItem,
        ) -> None:
            issuer = f"https://cognito-idp.us-east-1.amazonaws.com/{persisted_user.cognito_user_pool_id}"
            identifiers = user_context_service._get_user_identifiers(
                cookie="",
                username=persisted_user.username,
                issuer=issuer,
            )

            _, _, mock = central_api_auth_user_mock

            assert mock.call_count == 0
            assert identifiers == (
                str(persisted_user.account_uuid),
                str(persisted_user.organization_uuid),
            )

        def test_should_get_from_central_api(
            self,
            central_api_auth_user_mock: Tuple[str, str, _Matcher],
            non_persisted_user: UserItem,
        ) -> None:
            issuer = f"https://cognito-idp.us-east-1.amazonaws.com/{non_persisted_user.cognito_user_pool_id}"
            identifiers = user_context_service._get_user_identifiers(
                cookie="",
                username=non_persisted_user.username,
                issuer=issuer,
            )

            _, _, mock = central_api_auth_user_mock

            assert mock.called_once
            assert identifiers == (
                str(non_persisted_user.account_uuid),
                str(non_persisted_user.organization_uuid),
            )

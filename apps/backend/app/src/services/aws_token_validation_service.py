import base64
from typing import Any, Dict, List

import jwt
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerEventV2,
)
from jwt import PyJWK, PyJWKClient
from jwt.api_jwt import decode_complete

from src.exceptions.authorizer_exceptions import (
    AwsAccessTokenMissingFromCookie,
    AwsIdTokenMissingFromCookie,
    CookieHeaderMissing,
    InvalidAccessToken,
    TokenIssuerDifference,
)
from src.models.tokens.tokens import AwsTokens, UnverifiedTokens, VerifiedTokens
from src.services.idp_service import IDPService
from src.type_defs.decoded_jwts import (
    DecodedAwsAccessTokenTypeDef,
    DecodedAwsIdTokenTypeDef,
)


class AwsTokenValidationService:
    """
    Provides a list of method to retrieve and validate an AWS Token stored in
    a Cookie.
    """

    logger: Logger
    idp_service: IDPService

    def __init__(
        self,
        idp_service: IDPService,
        logger: Logger = Logger(),
    ) -> None:
        self.idp_service = idp_service
        self.logger = logger

    def _validate_cookie_header_present(self, headers: Dict[str, str]) -> None:
        """
        Validates if a Headers' Dictionary posses a `Cookie` key. If one is not
        present an Exception is raised.

        Raises:
            CookieHeaderMissing
        """
        if not headers.get("cookie"):
            raise CookieHeaderMissing

    def _get_aws_id_token_from_cookies_list(self, cookies: List[str] | None) -> str:
        """
        Retrieves value of a cookie with a key of `awsIdToken`. If one is not
        present, an Error is raised.

        Returns:
            str

        Raises:
            AwsIdTokenMissingFromCookie
        """
        if not cookies:
            raise AwsIdTokenMissingFromCookie

        try:
            cookie_with_token = next(
                cookie for cookie in cookies if cookie.startswith("awsIdToken=")
            )

            return cookie_with_token.replace("awsIdToken=", "")
        except StopIteration:
            raise AwsIdTokenMissingFromCookie

    def _get_aws_access_token_from_cookies_list(self, cookies: List[str] | None) -> str:
        """
        Retrieves value of a cookie with a key of `awsAccessToken`. If one is not
        present, an Error is raised.

        Returns:
            str

        Raises:
            AwsIdTokenMissingFromCookie
        """
        if not cookies:
            raise AwsAccessTokenMissingFromCookie

        try:
            cookie_with_token = next(
                cookie for cookie in cookies if cookie.startswith("awsAccessToken=")
            )

            return cookie_with_token.replace("awsAccessToken=", "")
        except StopIteration:
            raise AwsAccessTokenMissingFromCookie

    def _verify_matching_issuers(self, issuer_1: str, issuer_2: str) -> None:
        """
        Validates that two issuers match.

        Args:
            issuer_1 (str): First Issuer value to compare.
            issuer_2 (str): Second Issuer value to compare.

        Raises:
            TokenIssuerDifference: Raised when issuers do not match.

        """
        if issuer_1 != issuer_2:
            raise TokenIssuerDifference

    def _get_unverified_tokens(self, tokens: AwsTokens) -> UnverifiedTokens:
        """
        Retrieves a set of decoded and unverified tokens.

        Args:
            tokens (AwsTokens): A Tuple of tokens as strings.

        Returns:
            UnverifiedTokens(NamedTuple)

        """
        access_token, id_token = tokens

        unverified_access_token: DecodedAwsAccessTokenTypeDef = jwt.decode(
            access_token,
            verify=False,
            algorithms=["RS256"],
            options={"verify_signature": False},
        )
        unverified_id_token: DecodedAwsIdTokenTypeDef = jwt.decode(
            id_token,
            verify=False,
            algorithms=["RS256"],
            options={"verify_signature": False},
        )

        return UnverifiedTokens(
            access_token=unverified_access_token,
            id_token=unverified_id_token,
        )

    def _get_valid_issuer_from_token_issuer(self, issuer: str) -> str:
        """
        Validates that the issuer is an allowed Issuer, by finding them in our
        datastore of valid issuers. The issuer should be the base cognito-idp
        url.

        Args:
            issuer (str): Base url for the issuer.

        Returns:
            str: Validated issuer url as string.
        """
        idp_item = self.idp_service.get_idp_by_url(issuer)

        return f"{idp_item.url}/.well-known/jwks.json"

    def _decode_id_token_with_signing_key(
        self,
        id_token: str,
        signing_key: PyJWK,
    ) -> Dict[str, Any]:
        """
        Decodes an AWS ID Token with the provided signing key. Verifies that the
        key is valid, and returns a Dictionary that represents decoded token
        complete with headers.

        Args:
            id_token (str): String that represent ID Token

            sign_key (PyJwk): Represents a fetched JWK from PyJwt.

        Returns:
            (Dict[str, Any]): A Dictionary with the decoded token complete with
                headers.
        """

        return decode_complete(
            id_token,
            key=signing_key.key,
            algorithms=["RS256"],
            options={
                # "verify_exp": False,
                "verify_aud": False,
            },
        )

    def _validate_access_token_hash(
        self,
        access_token: str,
        decoded_id_token: Dict[str, Any],
    ) -> None:
        """
        Validates that an AWS Access Token via the AWS ID Token via the Access
        Token's hash.

        Raises:
            InvalidAccessToken: Occurs when hash comparison is invalid.
        """
        payload, header = decoded_id_token["payload"], decoded_id_token["header"]
        alg_obj = jwt.get_algorithm_by_name(header["alg"])
        digest = alg_obj.compute_hash_digest(
            access_token.encode("utf-8"),
        )

        hash_part = digest[: (len(digest) // 2)]
        at_hash = base64.urlsafe_b64encode(hash_part).decode().rstrip("=")

        if at_hash != payload["at_hash"]:
            raise InvalidAccessToken

    def _validate_token_against_cognito_pool(
        self,
        issuer_url: str,
        tokens: AwsTokens,
    ) -> VerifiedTokens:
        """
        Ensures that an issuer Identity Provider signed the supplied tokens.

        Args:
            issuer_url (str): The url of the IDP

            tokens (Tuple[str,str]): A tuple that represents the ID Token and
                access token.

        Returns:
            VerifiedTokens (Tuple[str, DecodedAwsIdToken])
        """
        jwks_client = PyJWKClient(issuer_url)

        signing_key = jwks_client.get_signing_key_from_jwt(tokens.id_token)

        data = self._decode_id_token_with_signing_key(tokens.id_token, signing_key)
        self._validate_access_token_hash(tokens.access_token, data)

        return VerifiedTokens(
            access_token=tokens.access_token,
            id_token=data["payload"],
        )

    def get_tokens_from_authorizer_event(
        self,
        event: APIGatewayAuthorizerEventV2,
    ) -> AwsTokens:
        """
        Retrieves tokens from the AwsAccessToken & AwsIdToken Cookies sent to
        the Authorizer.

        Args:
            event (APIGatewayAuthorizerEventV2): Authorization event with the
                cookies

        Returns:
            AwsTokens (NamedTuple): Tuple with tokens.
        """
        self._validate_cookie_header_present(event.headers)

        return AwsTokens(
            access_token=self._get_aws_access_token_from_cookies_list(event.cookies),
            id_token=self._get_aws_id_token_from_cookies_list(event.cookies),
        )

    def validate_tokens(self, tokens: AwsTokens) -> VerifiedTokens:
        """
        Accepts a tuple that represents an AWS ID Token and Access Token,
        and then:
            - verifies that the issuer is an allowed idp
            - that the tokens are valid and properly signed
            - and verifies the access token was minted by a trusted source.

        Returns
            VerifiedTokens: A Tuple that includes the validated decoded ID token
            and the access token (verified but not decoded).

        """
        unverified_tokens = self._get_unverified_tokens(tokens)

        self._verify_matching_issuers(
            unverified_tokens.access_token["iss"],
            unverified_tokens.id_token["iss"],
        )

        issuer_url = self._get_valid_issuer_from_token_issuer(
            unverified_tokens.id_token["iss"]
        )

        return self._validate_token_against_cognito_pool(
            issuer_url,
            tokens,
        )

import os
from typing import Any, Callable, Dict, List
from unittest.mock import Mock
from uuid import uuid4

import boto3
import pytest
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerEventV2,
)

from src.exceptions.authorizer_exceptions import (
    AwsIdTokenMissingFromCookie,
    CookieHeaderMissing,
    InvalidAccessToken,
    TokenIssuerDifference,
)
from src.exceptions.idp_exceptions import IDPNotFound
from src.models.dynamo.idp import IDPItem
from src.models.tokens.tokens import AwsTokens, VerifiedTokens
from src.services.aws_token_validation_service import (
    AwsAccessTokenMissingFromCookie,
    AwsTokenValidationService,
)
from src.services.idp_service import IDPService
from src.type_defs.decoded_jwts import (
    DecodedAwsAccessTokenTypeDef,
    DecodedAwsIdTokenTypeDef,
)
from tests.fixtures.tokens import RsaKeys
from tests.src.repositories.test_idp_repository import IDPRepository
from tests.stubs.http_api.authorization.http_api_authorizer_event_stub_builder import (
    HttpApiAuthorizerEventTypeDef,
)


class TestAwsTokenValidationService:
    class TestValidateCookieHeaderPresent:
        service = AwsTokenValidationService(idp_service=Mock())

        def test_should_not_raise(self) -> None:
            self.service._validate_cookie_header_present(
                {"cookie": str(uuid4())},
            )

        def test_should_raise_cookie_header_missing_exception(self) -> None:
            with pytest.raises(CookieHeaderMissing):
                self.service._validate_cookie_header_present({})

    class TestGetAwsIdTokenFromCookieList:
        service = AwsTokenValidationService(idp_service=Mock())

        @pytest.mark.parametrize(
            "cookies",
            [
                ["notAwsIdToken"],
                None,
            ],
        )
        def test_should_raise_aws_id_token_missing_from_cookie_error(
            self,
            cookies: List[str] | None,
        ) -> None:
            with pytest.raises(AwsIdTokenMissingFromCookie):
                self.service._get_aws_id_token_from_cookies_list(cookies)

        def test_should_return_aws_id_token(self) -> None:
            token_value = str(uuid4())
            id_token = f"awsIdToken={token_value}"
            cookies = ["something", "something", id_token]

            result = self.service._get_aws_id_token_from_cookies_list(cookies)

            assert result == token_value

    class TestGetAwsAccessTokenFromCookieList:
        service = AwsTokenValidationService(idp_service=Mock())

        @pytest.mark.parametrize(
            "cookies",
            [
                ["notAnAccessToken"],
                None,
            ],
        )
        def test_should_raise_access_token_missing_exception(
            self,
            cookies: List[str] | None,
        ) -> None:
            with pytest.raises(AwsAccessTokenMissingFromCookie):
                self.service._get_aws_access_token_from_cookies_list(cookies)

        def test_should_return_aws_access_token_from_cookies_list(self) -> None:
            token_value = str(uuid4())
            access_token = f"awsAccessToken={token_value}"
            cookies = ["something", "something", access_token]

            result = self.service._get_aws_access_token_from_cookies_list(cookies)

            assert result == token_value

    class TestGetUnverifiedTokens:
        service = AwsTokenValidationService(idp_service=Mock())

        def test_should_return_a_set_of_unverified_decoded_tokens(
            self,
            aws_access_token: str,
            aws_id_token: str,
            decoded_aws_access_token: DecodedAwsAccessTokenTypeDef,
            decoded_aws_id_token: DecodedAwsIdTokenTypeDef,
        ) -> None:
            response = self.service._get_unverified_tokens(
                AwsTokens(
                    access_token=aws_access_token,
                    id_token=aws_id_token,
                )
            )

            response.access_token == decoded_aws_access_token
            response.id_token == decoded_aws_id_token

        def test_should_handle_tokens_without_custom_role(
            self,
            aws_access_token: str,
            aws_id_token_without_role: str,
        ) -> None:
            response = self.service._get_unverified_tokens(
                AwsTokens(
                    access_token=aws_access_token,
                    id_token=aws_id_token_without_role,
                )
            )

            assert not response.id_token.get("custom:role")

    class TestVerifyIssuer:
        service = AwsTokenValidationService(idp_service=Mock())

        def test_verify_matching_issuer_should_succeed(self) -> None:
            issuer1 = "http://foo"
            issuer2 = issuer1
            self.service._verify_matching_issuers(issuer1, issuer2)

        def test_verify_matching_issuer_should_raise_token_issuer_difference(
            self,
        ) -> None:
            issuer1 = "http://foo1"
            issuer2 = "http://foo2"

            with pytest.raises(TokenIssuerDifference):
                self.service._verify_matching_issuers(issuer1, issuer2)

    class TestGetValidIssuerFromTokenIssuer:
        service = AwsTokenValidationService(
            idp_service=IDPService(
                repository=IDPRepository(
                    boto3.resource("dynamodb").Table(
                        os.environ["IDP_TABLE"],
                    ),
                )
            )
        )

        def test_should_get_valid_issuer(
            self,
            persisted_idp: IDPItem,
        ) -> None:
            url = self.service._get_valid_issuer_from_token_issuer(
                persisted_idp.url,
            )

            assert url == f"{persisted_idp.url}/.well-known/jwks.json"

        def test_should_raise_id_not_found_exception(self) -> None:
            url = "http://foo"

            with pytest.raises(IDPNotFound):
                self.service._get_valid_issuer_from_token_issuer(url)

    class TestDecodeIdTokenWithSigningKey:
        service = AwsTokenValidationService(idp_service=Mock())

        def test_should_decode_token_successfully(
            self,
            aws_id_token: str,
            complete_decoded_aws_id_token: Dict[str, Any],
            rsa_keys: RsaKeys,
        ) -> None:
            py_jwk_mock = Mock()
            py_jwk_mock.key = rsa_keys.public_key

            id_token = self.service._decode_id_token_with_signing_key(
                id_token=aws_id_token,
                signing_key=py_jwk_mock,  # type: ignore [arg-type]
            )

            assert id_token == complete_decoded_aws_id_token

    class TestValidateAccessTokenHash:
        service = AwsTokenValidationService(idp_service=Mock())

        def test_should_validate_at_hash(
            self,
            aws_access_token: str,
            complete_decoded_aws_id_token: Dict[str, Any],
            at_hash_patch: Callable[..., None],
        ) -> None:
            at_hash_patch()
            self.service._validate_access_token_hash(
                aws_access_token,
                complete_decoded_aws_id_token,
            )

        def test_should_raise_invalid_access_token(
            self,
            aws_access_token: str,
            complete_decoded_aws_id_token: Dict[str, Any],
        ) -> None:
            with pytest.raises(InvalidAccessToken):
                self.service._validate_access_token_hash(
                    aws_access_token,
                    complete_decoded_aws_id_token,
                )

    class TestValidateTokenAgainstCognitoPool:
        service = AwsTokenValidationService(idp_service=Mock())

        def test_should_use_pyjwk_client(
            self,
            aws_access_token: str,
            aws_id_token: str,
            py_jwk_client_mock: Mock,
            at_hash_patch: Callable[..., None],
        ) -> None:
            at_hash_patch()

            self.service._validate_token_against_cognito_pool(
                "http://foo",
                AwsTokens(
                    aws_access_token,
                    aws_id_token,
                ),
            )

    class TestGetTokensFromAuthorizerEvent:
        service = AwsTokenValidationService(idp_service=Mock())

        def test_should_succeed(
            self,
            aws_access_token: str,
            aws_id_token: str,
            authorizer_event_from_cookies_builder: Callable[
                [List[str]], HttpApiAuthorizerEventTypeDef
            ],
        ) -> None:
            event = authorizer_event_from_cookies_builder(
                [
                    f"awsAccessToken={aws_access_token}",
                    f"awsIdToken={aws_id_token}",
                ]
            )

            aws_tokens = self.service.get_tokens_from_authorizer_event(
                APIGatewayAuthorizerEventV2(event),  # type: ignore [arg-type]
            )

            assert aws_tokens == AwsTokens(
                access_token=aws_access_token,
                id_token=aws_id_token,
            )

    class TestValidateTokens:
        service = AwsTokenValidationService(
            idp_service=IDPService(
                repository=IDPRepository(
                    boto3.resource("dynamodb").Table(
                        os.environ["IDP_TABLE"],
                    ),
                )
            )
        )

        def test_should_succeed(
            self,
            aws_access_token: str,
            aws_id_token: str,
            decoded_aws_id_token: DecodedAwsIdTokenTypeDef,
            at_hash_patch: Callable[..., None],
            py_jwk_client_mock: Mock,
            persisted_idp: IDPItem,
        ) -> None:
            at_hash_patch()

            verified_tokens = self.service.validate_tokens(
                AwsTokens(
                    access_token=aws_access_token,
                    id_token=aws_id_token,
                )
            )

            assert verified_tokens == VerifiedTokens(
                id_token=decoded_aws_id_token,
                access_token=aws_access_token,
            )

        def test_should_raise_token_issuer_difference(
            self,
            aws_access_token_bad_issuer: str,
            aws_id_token: str,
        ) -> None:
            with pytest.raises(TokenIssuerDifference):
                self.service.validate_tokens(
                    AwsTokens(
                        access_token=aws_access_token_bad_issuer,
                        id_token=aws_id_token,
                    )
                )

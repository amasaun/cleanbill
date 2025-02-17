from typing import Any, Callable, Dict, List, Tuple, Type
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerEventV2,
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from pytest_mock import MockerFixture
from requests_mock.adapter import _Matcher

from src.authorizer.index import (
    aws_token_validation_service,
    handler as strict_authorizer,
    user_context_service,
)
from src.exceptions.authorizer_exceptions import AuthorizationException
from src.exceptions.central_api_exceptions import CentralApiExceptions
from src.exceptions.idp_exceptions import IDPException
from src.models.dynamo.idp import IDPItem
from src.models.user_context.user_context import UserContext
from src.type_defs.authorizer_responses import APIGatewayAuthorizerResponseV2TypeDef
from tests.fixtures.tokens import CookieComponents
from tests.stubs.http_api.authorization.http_api_authorizer_event_stub_builder import (
    HttpApiAuthorizerEventTypeDef,
)


class TestStrictAuthorizer:
    def test_strict_authorizer_should_return_allow_with_context(
        self,
        at_hash_patch: Callable[..., None],
        authorizer_event_from_cookies_builder: Callable[
            [List[str]], HttpApiAuthorizerEventTypeDef
        ],
        cookie_components: CookieComponents,
        central_api_auth_user_mock: Tuple[str, str, _Matcher],
        mock_context: LambdaContext,
        user_context_callable: Callable[[str, str, str], UserContext],
        persisted_idp: IDPItem,
        py_jwk_client_mock: Mock,
    ) -> None:
        event = authorizer_event_from_cookies_builder(
            cookie_components.cookie_list,
        )

        account_uuid, organization_uuid, _ = central_api_auth_user_mock
        at_hash_patch()

        response = strict_authorizer(
            APIGatewayAuthorizerEventV2(
                event,  # type: ignore [arg-type]
            ),
            mock_context,
        )

        expected_response: APIGatewayAuthorizerResponseV2TypeDef = {
            "isAuthorized": True,
            "context": user_context_callable(
                account_uuid,
                organization_uuid,
                cookie_components.cookie,
            ).context(),  # type: ignore[typeddict-item]
        }

        assert response == expected_response

    def test_strict_authorizer_should_return_allow_with_no_custom_role(
        self,
        at_hash_patch: Callable[..., None],
        authorizer_event_from_cookies_builder: Callable[
            [List[str]], HttpApiAuthorizerEventTypeDef
        ],
        cookie_components_without_role: CookieComponents,
        central_api_auth_user_mock: Tuple[str, str, _Matcher],
        mock_context: LambdaContext,
        user_context_callable_without_role: Callable[[str, str, str], UserContext],
        persisted_idp: IDPItem,
        py_jwk_client_mock: Mock,
    ) -> None:
        event = authorizer_event_from_cookies_builder(
            cookie_components_without_role.cookie_list,
        )

        account_uuid, organization_uuid, _ = central_api_auth_user_mock
        at_hash_patch()

        response = strict_authorizer(
            APIGatewayAuthorizerEventV2(
                event,  # type: ignore [arg-type]
            ),
            mock_context,
        )

        expected_response: APIGatewayAuthorizerResponseV2TypeDef = {
            "isAuthorized": True,
            "context": user_context_callable_without_role(
                account_uuid,
                organization_uuid,
                cookie_components_without_role.cookie,
            ).context(),  # type: ignore[typeddict-item]
        }

        assert response == expected_response

    @pytest.mark.parametrize(
        "exception",
        [
            AuthorizationException,
            CentralApiExceptions,
            IDPException,
        ],
    )
    def test_strict_authorizer_should_return_deny(
        self,
        authorizer_event_from_cookies_builder: Callable[
            [List[str]], HttpApiAuthorizerEventTypeDef
        ],
        cookie_components: CookieComponents,
        exception: Type[Exception],
        mock_context: LambdaContext,
        monkeypatch: MonkeyPatch,
    ) -> None:
        def _raise_exception(
            *args: List[Any],
            **kwargs: Dict[str, Any],
        ) -> None:
            raise exception

        from src.services.aws_token_validation_service import AwsTokenValidationService

        monkeypatch.setattr(
            AwsTokenValidationService,
            "get_tokens_from_authorizer_event",
            _raise_exception,
        )

        event = authorizer_event_from_cookies_builder(
            cookie_components.cookie_list,
        )

        response = strict_authorizer(
            APIGatewayAuthorizerEventV2(
                event,  # type: ignore [arg-type]
            ),
            mock_context,
        )

        assert response == {
            "isAuthorized": False,
        }

    def test_strict_authorizer_handles_warmer_event(
        self,
        mock_context: LambdaContext,
        mocker: MockerFixture,
    ) -> None:
        token_validate_spy = mocker.spy(
            aws_token_validation_service,
            "get_tokens_from_authorizer_event",
        )

        user_context_spy = mocker.spy(
            user_context_service,
            "user_context_from_verified_tokens",
        )

        event = {"warmer": True}

        response = strict_authorizer(event, mock_context)

        assert response is None
        user_context_spy.assert_not_called()
        token_validate_spy.assert_not_called()

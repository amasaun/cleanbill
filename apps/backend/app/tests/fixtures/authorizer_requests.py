from typing import Any, Callable, Dict, List

import pytest

from tests.stubs.http_api.authorization.http_api_authorizer_event_stub_builder import (
    HttpApiAuthorizerEventStubBuilder,
    HttpApiAuthorizerEventTypeDef,
)


@pytest.fixture
def simple_authorizer_event() -> HttpApiAuthorizerEventTypeDef:
    return HttpApiAuthorizerEventStubBuilder().build()


@pytest.fixture
def authorizer_event_from_cookies_builder() -> (
    Callable[
        [List[str]],
        HttpApiAuthorizerEventTypeDef,
    ]
):
    def _event_from_cookies(
        cookies: List[str],
    ) -> HttpApiAuthorizerEventTypeDef:
        cookie = "; ".join(cookies)
        return (
            HttpApiAuthorizerEventStubBuilder()
            .identity_source([cookie])
            .headers({"cookie": cookie})
            .cookies(cookies)
            .build()
        )

    return _event_from_cookies

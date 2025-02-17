from __future__ import annotations

from typing import Dict, List, Literal, NotRequired, Optional, TypedDict
from uuid import uuid4

from tests.stubs.http_api.authorization.http_authorizer_request_context import (
    HttpAuthorizerRequestContextStubBuilder,
    HttpAuthorizerRequestContextTypeDef,
)

HttpApiAuthorizerEventTypeDef = TypedDict(
    "HttpApiAuthorizerEventTypeDef",
    {
        "cookies": List[str],
        "headers": Dict[str, str],
        "identitySource": List[str],
        "pathParameters": NotRequired[Dict[str, str]],
        "queryStringParameters": NotRequired[Dict[str, str]],
        "rawPath": str,
        "requestContext": HttpAuthorizerRequestContextTypeDef,
        "routeArn": str,
        "routeKey": str,
        "stageVariables": NotRequired[Dict[str, str]],
        "type": Literal["REQUEST"],
        "version": str,
    },
)


class HttpApiAuthorizerEventStubBuilder:
    """
    Builds a Dictionary that represents the payload sent to an Authorizer in
    version 2.0.

    Reference:
     - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html
    """

    _cookies: List[str]
    _headers: Dict[str, str]
    _identity_source: List[str]
    _path_parameters: Optional[Dict[str, str]]
    _query_string_parameters: Optional[Dict[str, str]]
    _raw_path: str
    _request_context: HttpAuthorizerRequestContextTypeDef
    _route_arn: str
    _route_key: str
    _stage_variables: Optional[Dict[str, str]]
    _type: Literal["REQUEST"]
    _version: str

    def __init__(self) -> None:
        request_context = HttpAuthorizerRequestContextStubBuilder().build()
        self._cookies = []
        self._headers = {"accept": "*/*"}
        self._identity_source = []
        self._path_parameters = None
        self._query_string_parameters = None
        self._raw_path = "api/test"
        self._request_context = request_context
        self._route_arn = (
            f"arn:aws:execute-api:us-east-1:123456789:{uuid4()}/$default/GET/api/test"
        )
        self._route_key = request_context["routeKey"]
        self._stage_variables = None
        self._type = "REQUEST"
        self._version = "2.0"

    def cookies(self, cookies: List[str]) -> HttpApiAuthorizerEventStubBuilder:
        self._cookies = cookies
        return self

    def headers(self, headers: Dict[str, str]) -> HttpApiAuthorizerEventStubBuilder:
        self._headers = headers
        return self

    def identity_source(
        self, identity_source: List[str]
    ) -> HttpApiAuthorizerEventStubBuilder:
        self._identity_source = identity_source
        return self

    def raw_path(self, raw_path: str) -> HttpApiAuthorizerEventStubBuilder:
        self._raw_path = raw_path
        return self

    def request_context(
        self,
        request_context: HttpAuthorizerRequestContextTypeDef,
    ) -> HttpApiAuthorizerEventStubBuilder:
        self._request_context = request_context
        return self

    def route_arn(self, route_arn: str) -> HttpApiAuthorizerEventStubBuilder:
        self._route_arn = route_arn
        return self

    def route_key(self, route_key: str) -> HttpApiAuthorizerEventStubBuilder:
        self._route_key = route_key
        return self

    def type(self, type: Literal["REQUEST"] | str) -> HttpApiAuthorizerEventStubBuilder:
        self._type = type  # type: ignore[assignment]
        return self

    def version(self, version: str) -> HttpApiAuthorizerEventStubBuilder:
        self._version = version
        return self

    def build(self) -> HttpApiAuthorizerEventTypeDef:
        event: HttpApiAuthorizerEventTypeDef = {
            "cookies": self._cookies,
            "headers": self._headers,
            "identitySource": self._identity_source,
            "rawPath": self._raw_path,
            "requestContext": self._request_context,
            "routeArn": self._route_arn,
            "routeKey": self._route_key,
            "type": self._type,
            "version": self._version,
        }

        if self._path_parameters:
            event.update({"pathParameters": self._path_parameters})

        if self._query_string_parameters:
            event.update({"queryStringParameters": self._query_string_parameters})

        if self._stage_variables:
            event.update({"stageVariables": self._stage_variables})

        return event

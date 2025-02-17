from __future__ import annotations

from typing import Dict, List, Literal, Optional, cast

from src.type_defs.http_api_event import (
    HttpApiEventHeaders,
    HttpApiEventTypDef,
    HttpApiRequestContextTypeDef,
)


class HttpApiEventStubBuilder:
    """
    Stubs out the HttpApi V2 event.

    Reference:
    https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    """

    _version: Literal["2.0"]
    _route_key: str
    _raw_path: str
    _raw_query_string: str
    _cookies: List[str]
    _headers: HttpApiEventHeaders
    _query_string_parameters: Dict[str, str]
    _request_context: HttpApiRequestContextTypeDef
    _body: Optional[str]
    _path_paramters: Optional[Dict[str, str]]
    _is_base_64_encoded: bool
    _stage_variables: Dict[str, str]

    def __init__(self) -> None:
        self._version = "2.0"
        self._route_key = "GET api/foo"
        self._raw_path = "api/foo"
        self._raw_query_string = ""
        self._cookies = []
        self._headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "content-length": "0",
            "host": "some_id.execute-api.us-east-1.amazonaws.com",
            "user-agent": "python-requests/2.31.0",
            "x-amzn-trace-id": "Root=some-id",
            "x-forwarded-for": "127.0.0.01",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https",
        }
        self._request_context

    def build(self) -> HttpApiEventTypDef:
        data = {
            "version": self._version,
            "routKey": self._route_key,
            "rawPath": self._raw_path,
            "rawQueryString": self._raw_query_string,
            "cookies": self._cookies,
            "headers": self._headers,
            "queryStringParameters": self._query_string_parameters,
            "requestContext": self._request_context,
            "body": self._body,  # type: ignore [typeddict-item]
            "isBase64Encoded": self._is_base_64_encoded,
            "stageVariables": self._stage_variables,
        }

        return cast(
            HttpApiEventTypDef,
            {k: v for k, v in data.items() if v is not None},
        )

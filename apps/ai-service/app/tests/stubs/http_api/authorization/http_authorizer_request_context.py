from __future__ import annotations

from datetime import datetime
from typing import TypedDict
from uuid import uuid4

from tests.stubs.http_api.authorization.http_request_stub_builder import (
    HttpRequestStubBuilder,
    HttpRequestTypeDef,
)

HttpAuthorizerRequestContextTypeDef = TypedDict(
    "HttpAuthorizerRequestContextTypeDef",
    {
        "accountId": str,
        "apiId": str,
        "domainName": str,
        "domainPrefix": str,
        "http": HttpRequestTypeDef,
        "requestId": str,
        "routeKey": str,
        "stage": str,
        "time": str,
        "timeEpoch": int,
    },
)


class HttpAuthorizerRequestContextStubBuilder:
    _account_id: str
    _api_id: str
    _domain_name: str
    _domain_prefix: str
    _http: HttpRequestTypeDef
    _request_id: str
    _route_key: str
    _stage: str
    _time: str
    _time_epoch: int

    def _datetime_to_str(self, dt: datetime) -> str:
        return dt.strftime("%d/%b/%Y:%H:%M:%S %z")

    def _datetime_to_epoch(self, dt: datetime) -> int:
        return int(dt.strftime("%s"))

    def __init__(self) -> None:
        http_request = HttpRequestStubBuilder().build()
        now = datetime.utcnow()
        self._account_id = "123456789"
        self._api_id = str(uuid4())
        self._domain_name = str(uuid4())
        self._domain_prefix = str(uuid4())
        self._http = http_request
        self._request_id = str(uuid4())
        self._route_key = f"{http_request['method']} /api/test"
        self._stage = "$default"
        self._time = self._datetime_to_str(now)
        self._time_epoch = self._datetime_to_epoch(now)

    def account_id(self, account_id: str) -> HttpAuthorizerRequestContextStubBuilder:
        self._account_id = account_id
        return self

    def api_id(self, api_id: str) -> HttpAuthorizerRequestContextStubBuilder:
        self._api_id = api_id
        return self

    def domain_name(self, domain_name: str) -> HttpAuthorizerRequestContextStubBuilder:
        self._domain_name = domain_name
        return self

    def http(self, http: HttpRequestTypeDef) -> HttpAuthorizerRequestContextStubBuilder:
        self._http = http
        return self

    def request_id(self, request_id: str) -> HttpAuthorizerRequestContextStubBuilder:
        self._request_id = request_id
        return self

    def route_key(self, route_key: str) -> HttpAuthorizerRequestContextStubBuilder:
        self._route_key = route_key
        return self

    def stage(self, stage: str) -> HttpAuthorizerRequestContextStubBuilder:
        self._stage = stage
        return self

    def time(self, dt: datetime) -> HttpAuthorizerRequestContextStubBuilder:
        self._time = self._datetime_to_str(dt)
        return self

    def time_epoch(self, dt: datetime) -> HttpAuthorizerRequestContextStubBuilder:
        self._time_epoch = self._datetime_to_epoch(dt)
        return self

    def build(self) -> HttpAuthorizerRequestContextTypeDef:
        return {
            "accountId": self._account_id,
            "apiId": self._api_id,
            "domainName": self._domain_name,
            "domainPrefix": self._domain_prefix,
            "http": self._http,
            "requestId": self._request_id,
            "routeKey": self._route_key,
            "stage": self._stage,
            "time": self._time,
            "timeEpoch": self._time_epoch,
        }

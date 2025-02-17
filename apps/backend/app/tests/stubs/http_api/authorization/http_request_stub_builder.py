from __future__ import annotations

from typing import Literal, TypeAlias, TypedDict

RequestMethod: TypeAlias = Literal["GET", "POST", "PATCH", "DELETE", "OPTIONS", "PUT"]

HttpRequestTypeDef = TypedDict(
    "HttpRequestTypeDef",
    {
        "method": RequestMethod,
        "path": str,
        "protocol": str,
        "sourceIp": str,
        "userAgent": str,
    },
)


class HttpRequestStubBuilder:
    _method: RequestMethod
    _path: str
    _protocol: str
    _source_ip: str
    _user_agent: str

    def __init__(self) -> None:
        self._method = "GET"
        self._path = "/api/test"
        self._protocol = "HTTP/1.1"
        self._source_ip = "127.0.0.1"
        self._user_agent = "PostmanRuntime/7.32.3"

    def method(self, method: RequestMethod) -> HttpRequestStubBuilder:
        self._method = method
        return self

    def path(self, path: str) -> HttpRequestStubBuilder:
        self._path = path
        return self

    def protocol(self, protocol: str) -> HttpRequestStubBuilder:
        self._protocol = protocol
        return self

    def source_ip(self, source_ip: str) -> HttpRequestStubBuilder:
        self._source_ip = source_ip
        return self

    def user_agent(self, user_agent: str) -> HttpRequestStubBuilder:
        self._user_agent = user_agent
        return self

    def build(self) -> HttpRequestTypeDef:
        return {
            "method": self._method,
            "path": self._path,
            "protocol": self._protocol,
            "sourceIp": self._source_ip,
            "userAgent": self._user_agent,
        }

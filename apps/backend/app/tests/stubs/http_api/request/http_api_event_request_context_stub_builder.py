from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import uuid4

from src.type_defs.http_api_event import (
    HttpApiRequestContextAuthenticationTypeDef,
    HttpApiRequestContextHttpTypeDef,
    HttpApiRequestContextLambdaAuthorizerTypeDef,
    HttpApiRequestContextTypeDef,
)


class HttpApiEventRequestContextStubBuilder:
    _account_id: str
    _api_id: str
    _authentication: Optional[HttpApiRequestContextAuthenticationTypeDef]
    _authorizer: HttpApiRequestContextLambdaAuthorizerTypeDef
    _domain_name: str
    _domain_prefix: str
    _http: HttpApiRequestContextHttpTypeDef
    _request_id: str
    _route_key: str
    _stage: str
    _time: str
    _time_epoch: int

    def _default_authorizer(self) -> Dict[str, Any]:
        return {
            "accountUuid": "ae320eb3-dab5-41ca-84ad-c5cba9df983a",
            "cookie": "; ".join(
                [
                    "awsRefreshToken=some_token"
                    f"tokenExpiration={(datetime.now() + timedelta(hours=1)).isoformat()}"
                    "awsIdToken=some_token"
                    "awsAccessToken=some_token"
                ]
            ),
            "email": "fry.example.com",
            "firstName": "fry",
            "lastName": "futurama",
            "role": "Deep6SuperUser",
            "user_claims": {
                "buildQuery": True,
                "canShare": False,
                "downloadData": True,
                "irbMemberships": [""],
                "phiAccessLevel": "PATIENT_LEVEL_FULL",
                "validateData": True,
                "versionView": True,
            },
            "username": "someone",
        }

    def _default_http(self) -> HttpApiRequestContextHttpTypeDef:
        return {
            "method": "GET",
            "path": "/api/study-membership",
            "protocol": "HTTP/1.1",
            "sourceIp": "173.30.81.144",
            "userAgent": "python-requests/2.31.0",
        }

    def __init__(self) -> None:
        self._account_id = "123456789"
        self._api_id = str(uuid4())
        self._authentication = None
        self._authorizer = {"lambda": self._default_authorizer()}
        self._domain_prefix = "foo"
        self._domain_name = f"{self._domain_prefix}.execute-api.us-east-1.amazonaws.com"
        self._http = self._default_http()
        self._request_id = str(uuid4())
        self._route_key = "GET /api/foo"
        self._stage = "$default"
        self._time = "10/Nov/2023:04:40:00 +0000"
        self._time_epoch = int((datetime.now() - timedelta(minutes=15)).strftime("%s"))

    def build(self) -> HttpApiRequestContextTypeDef:
        return {
            "accountId": self._account_id,
            "apiId": self._api_id,
            "authentication": self._authentication,  # type: ignore [typeddict-item]
            "authorizer": self._authorizer,
            "domainName": self._domain_name,
            "domainPrefix": self._domain_prefix,
            "http": self._http,
            "requestId": self._request_id,
            "routeKey": self._route_key,
            "stage": self._stage,
            "time": self._time,
            "timeEpoch": self._time_epoch,
        }

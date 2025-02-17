from __future__ import annotations

import os
from datetime import datetime, timedelta
from uuid import uuid4

from src.type_defs.decoded_jwts import PreDecodedAwsAccessTokenTypeDef


class PreDecodedAccessTokenStubBuilder:
    _auth_time: int | float
    _client_id: str
    _event_id: str
    _exp: datetime | int | float
    _iat: datetime | int | float
    _issuer: str
    _jti: str
    _origin_jti: str
    _scope: str
    _sub: str
    _token_use: str
    _username: str
    _version: int

    def __init__(self) -> None:
        now = datetime.utcnow()

        self._auth_time = now.timestamp()
        self._client_id = str(uuid4())
        self._event_id = str(uuid4())
        self._exp = now + timedelta(hours=1)
        self._iat = now
        self._issuer = os.environ["ISSUER_URL"]
        self._jti = str(uuid4())
        self._origin_jti = str(uuid4())
        self._scope = "aws.cognito.signin.user.admin phone openid profile email"
        self._sub = str(uuid4())
        self._token_use = "access"
        self._username = "phillip.fry@foo-test.com"
        self._version = 2

    def auth_time(self, auth_time: datetime) -> PreDecodedAccessTokenStubBuilder:
        self._auth_time = auth_time.timestamp()
        return self

    def client_id(self, client_id: str) -> PreDecodedAccessTokenStubBuilder:
        self._client_id = client_id
        return self

    def event_id(self, event_id: str) -> PreDecodedAccessTokenStubBuilder:
        self._event_id = event_id
        return self

    def exp(self, exp: datetime) -> PreDecodedAccessTokenStubBuilder:
        self._exp = exp
        return self

    def iat(self, issued_at: datetime) -> PreDecodedAccessTokenStubBuilder:
        self._iat = issued_at
        return self

    def issuer(self, issuer: str) -> PreDecodedAccessTokenStubBuilder:
        self._issuer = issuer
        return self

    def jti(self, jti: str) -> PreDecodedAccessTokenStubBuilder:
        self._jti = jti
        return self

    def origin_jti(self, origin_jti: str) -> PreDecodedAccessTokenStubBuilder:
        self._origin_jti = origin_jti
        return self

    def scope(self, scope: str) -> PreDecodedAccessTokenStubBuilder:
        self._scope = scope
        return self

    def sub(self, subject: str) -> PreDecodedAccessTokenStubBuilder:
        self._sub = subject
        return self

    def token_use(self, token_use: str) -> PreDecodedAccessTokenStubBuilder:
        self._token_use = token_use
        return self

    def username(self, username: str) -> PreDecodedAccessTokenStubBuilder:
        self._username = username
        return self

    def version(self, version: int) -> PreDecodedAccessTokenStubBuilder:
        self._version = version
        return self

    def build(self) -> PreDecodedAwsAccessTokenTypeDef:
        return {
            "auth_time": self._auth_time,
            "client_id": self._client_id,
            "event_id": self._event_id,
            "exp": self._exp,
            "iat": self._iat,
            "iss": self._issuer,
            "jti": self._jti,
            "origin_jti": self._origin_jti,
            "scope": self._scope,
            "sub": self._sub,
            "token_use": self._token_use,
            "username": self._username,
            "version": self._version,
        }

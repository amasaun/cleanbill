from __future__ import annotations

import os
from datetime import datetime, timedelta
from uuid import uuid4

from src.common.phi_access_level import PhiAccessLevel
from src.type_defs.decoded_jwts import PreDecodedAwsIdTokenTypeDef


class PreDecodedIdTokenStubBuilder:
    _at_hash: str | None
    _aud: str
    _auth_time: float
    _cognito_username: str
    _custom_auditing_logs: str
    _custom_build_query: str
    _custom_can_share: str
    _custom_download_data: str
    _custom_irb_memberships: str
    _custom_phi_access_level: str
    _custom_role: str
    _custom_share_recipient: str
    _custom_tr_access: str
    _custom_validate_data: str
    _custom_version_view: str
    _email: str
    _event_id: str
    _exp: datetime | int
    _family_name: str
    _given_name: str
    _iat: datetime | int
    _issuer: str
    _jti: str
    _origin_jti: str
    _sub: str
    _token_use: str

    def __init__(self) -> None:
        email_and_username = "phillip.fry@foo-test.com"
        now = datetime.utcnow()

        self._aud = str(uuid4())
        self._auth_time = now.timestamp()
        self._cognito_username = email_and_username
        self._custom_auditing_logs = "true"
        self._custom_auditing_logs = "true"
        self._custom_build_query = "true"
        self._custom_can_share = "true"
        self._custom_download_data = "true"
        self._custom_irb_memberships = ""
        self._custom_phi_access_level = "PATIENT_LEVEL_FULL"
        self._custom_role = "Deep6SuperUser"
        self._custom_share_recipient = "true"
        self._custom_tr_access = "true"
        self._custom_validate_data = "true"
        self._custom_version_view = "true"
        self._email = email_and_username
        self._event_id = str(uuid4())
        self._exp = now + timedelta(hours=1)
        self._family_name = "fry"
        self._given_name = "phillip"
        self._iat = now
        self._issuer = os.environ["ISSUER_URL"]
        self._jti = str(uuid4())
        self._origin_jti = str(uuid4())
        self._sub = str(uuid4())
        self._token_use = "id"

    @staticmethod
    def _bool_to_str(a_bool: bool) -> str:
        return str(a_bool).lower()

    def at_hash(self, hash: str | None) -> PreDecodedIdTokenStubBuilder:
        self._at_hash = hash
        return self

    def aud(self, aud: str) -> PreDecodedIdTokenStubBuilder:
        self._aud = aud
        return self

    def auth_time(self, auth_time: datetime) -> PreDecodedIdTokenStubBuilder:
        self._auth_time = auth_time.timestamp()
        return self

    def cognito_username(self, username: str) -> PreDecodedIdTokenStubBuilder:
        self._cognito_username = username
        return self

    def custom_auditing_log(self, auditing_logs: bool) -> PreDecodedIdTokenStubBuilder:
        self._custom_auditing_logs = self._bool_to_str(auditing_logs)
        return self

    def custom_build_query(self, build_query: bool) -> PreDecodedIdTokenStubBuilder:
        self._custom_build_query = self._bool_to_str(build_query)
        return self

    def custom_can_share(self, can_share: bool) -> PreDecodedIdTokenStubBuilder:
        self._custom_can_share = self._bool_to_str(can_share)
        return self

    def custom_download_data(self, download_data: bool) -> PreDecodedIdTokenStubBuilder:
        self._custom_download_data = self._bool_to_str(download_data)
        return self

    def custom_irb_memberships(
        self, irb_memberships: str
    ) -> PreDecodedIdTokenStubBuilder:
        self._custom_irb_memberships = irb_memberships
        return self

    def phi_level_access(
        self, phi_level_access: PhiAccessLevel
    ) -> PreDecodedIdTokenStubBuilder:
        self._custom_phi_access_level = phi_level_access
        return self

    def custom_role(self, role: str) -> PreDecodedIdTokenStubBuilder:
        self._custom_role = role
        return self

    def custom_share_recipient(
        self, share_recipient: bool
    ) -> PreDecodedIdTokenStubBuilder:
        self._custom_share_recipient = self._bool_to_str(share_recipient)
        return self

    def custom_tr_access(self, tr_access: bool) -> PreDecodedIdTokenStubBuilder:
        self._custom_tr_access = self._bool_to_str(tr_access)
        return self

    def custom_validate_data(self, validate_data: bool) -> PreDecodedIdTokenStubBuilder:
        self._custom_validate_data = self._bool_to_str(validate_data)
        return self

    def custom_version_view(self, version_view: bool) -> PreDecodedIdTokenStubBuilder:
        self._custom_version_view = self._bool_to_str(version_view)
        return self

    def email(self, email: str) -> PreDecodedIdTokenStubBuilder:
        self._email = email
        return self

    def event_id(self, event_id: str) -> PreDecodedIdTokenStubBuilder:
        self._event_id = event_id
        return self

    def exp(self, expiration: datetime) -> PreDecodedIdTokenStubBuilder:
        self._exp = expiration
        return self

    def family_name(self, family_name: str) -> PreDecodedIdTokenStubBuilder:
        self._family_name = family_name
        return self

    def given_name(self, given_name: str) -> PreDecodedIdTokenStubBuilder:
        self._given_name = given_name
        return self

    def iat(self, issued_at: datetime) -> PreDecodedIdTokenStubBuilder:
        self._iat = issued_at
        return self

    def issuer(self, issuer: str) -> PreDecodedIdTokenStubBuilder:
        self._issuer = issuer
        return self

    def jti(self, jti: str) -> PreDecodedIdTokenStubBuilder:
        self._jti = jti
        return self

    def origin_jti(self, origin_jti: str) -> PreDecodedIdTokenStubBuilder:
        self._origin_jti = origin_jti
        return self

    def sub(self, sub: str) -> PreDecodedIdTokenStubBuilder:
        self._sub = sub
        return self

    def token_use(self, token_use: str) -> PreDecodedIdTokenStubBuilder:
        self._token_use = token_use
        return self

    def build(self) -> PreDecodedAwsIdTokenTypeDef:
        return {
            "at_hash": "",
            "aud": self._aud,
            "auth_time": self._auth_time,
            "cognito:username": self._cognito_username,
            "custom:auditing_logs": self._custom_auditing_logs,
            "custom:build_query": self._custom_build_query,
            "custom:can_share": self._custom_can_share,
            "custom:download_data": self._custom_download_data,
            "custom:irb_memberships": self._custom_irb_memberships,
            "custom:phi_access_level": self._custom_phi_access_level,
            "custom:role": self._custom_role,
            "custom:share_recipient": self._custom_share_recipient,
            "custom:tr_access": self._custom_tr_access,
            "custom:validate_data": self._custom_validate_data,
            "custom:version_view": self._custom_version_view,
            "email": self._email,
            "event_id": self._event_id,
            "exp": self._exp,
            "family_name": self._family_name,
            "given_name": self._given_name,
            "iat": self._iat,
            "iss": self._issuer,
            "jti": self._jti,
            "origin_jti": self._origin_jti,
            "sub": self._sub,
            "token_use": self._token_use,
        }

    def build_without_role(self) -> PreDecodedAwsIdTokenTypeDef:
        return {
            "at_hash": "",
            "aud": self._aud,
            "auth_time": self._auth_time,
            "cognito:username": self._cognito_username,
            "custom:auditing_logs": self._custom_auditing_logs,
            "custom:build_query": self._custom_build_query,
            "custom:can_share": self._custom_can_share,
            "custom:download_data": self._custom_download_data,
            "custom:irb_memberships": self._custom_irb_memberships,
            "custom:phi_access_level": self._custom_phi_access_level,
            "custom:share_recipient": self._custom_share_recipient,
            "custom:tr_access": self._custom_tr_access,
            "custom:validate_data": self._custom_validate_data,
            "custom:version_view": self._custom_version_view,
            "email": self._email,
            "event_id": self._event_id,
            "exp": self._exp,
            "family_name": self._family_name,
            "given_name": self._given_name,
            "iat": self._iat,
            "iss": self._issuer,
            "jti": self._jti,
            "origin_jti": self._origin_jti,
            "sub": self._sub,
            "token_use": self._token_use,
        }

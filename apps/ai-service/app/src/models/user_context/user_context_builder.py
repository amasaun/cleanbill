from __future__ import annotations

from src.exceptions.user_context_exceptions import UserContextException
from src.models.user_context.user_claims_context import UserClaimsContext
from src.models.user_context.user_context import UserContext, UserContextTypeDef


class UserContextBuilder:
    _account_uuid: str
    _cookie: str
    _email: str
    _first_name: str
    _last_name: str
    _organization_uuid: str
    _role: str
    _user_claims: UserClaimsContext
    _username: str

    def account_uuid(self, account_uuid: str) -> UserContextBuilder:
        self._account_uuid = account_uuid
        return self

    def cookie(self, cookie: str) -> UserContextBuilder:
        self._cookie = cookie
        return self

    def email(self, email: str) -> UserContextBuilder:
        self._email = email
        return self

    def first_name(self, first_name: str) -> UserContextBuilder:
        self._first_name = first_name
        return self

    def last_name(self, last_name: str) -> UserContextBuilder:
        self._last_name = last_name
        return self

    def organization_uuid(self, organization_uuid: str) -> UserContextBuilder:
        self._organization_uuid = organization_uuid
        return self

    def role(self, role: str) -> UserContextBuilder:
        self._role = role
        return self

    def user_claims(self, claims: UserClaimsContext) -> UserContextBuilder:
        self._user_claims = claims
        return self

    def username(self, username: str) -> UserContextBuilder:
        self._username = username
        return self

    def _validate_values(self) -> None:
        for attr, value in self.__dict__.items():
            if value is None:
                raise UserContextException(f"{attr} cannot be null")

    def build(self) -> UserContext:
        self._validate_values()

        return UserContext(
            account_uuid=self._account_uuid,
            cookie=self._cookie,
            email=self._email,
            first_name=self._first_name,
            last_name=self._last_name,
            organization_uuid=self._organization_uuid,
            role=self._role,
            user_claims=self._user_claims,
            username=self._username,
        )

    def build_context(self) -> UserContextTypeDef:
        return self.build().context()

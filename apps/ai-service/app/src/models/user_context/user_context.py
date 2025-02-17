from typing import TypedDict, cast

from pydantic import Field

from src.models.user_context.context_base_model import ContextBaseModel
from src.models.user_context.user_claims_context import (
    UserClaimsContext,
    UserClaimsTypeDef,
)

UserContextTypeDef = TypedDict(
    "UserContextTypeDef",
    {
        "accountUuid": str,
        "cookie": str,
        "email": str,
        "firstName": str,
        "lastName": str,
        "organizationUuid": str,
        "role": str,
        "user_claims": UserClaimsTypeDef,
        "username": str,
    },
)


class UserContext(ContextBaseModel):
    account_uuid: str = Field(alias="accountUuid")
    cookie: str
    email: str
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    organization_uuid: str = Field(alias="organizationUuid")
    role: str
    user_claims: UserClaimsContext
    username: str

    def context(self) -> UserContextTypeDef:
        return cast(
            UserContextTypeDef,
            self.dict(by_alias=True),
        )

from typing import List, TypedDict, cast

from pydantic import Field

from src.common.phi_access_level import PhiAccessLevel
from src.models.user_context.context_base_model import ContextBaseModel

UserClaimsTypeDef = TypedDict(
    "UserClaimsTypeDef",
    {
        "buildQuery": bool,
        "canShare": bool,
        "irbMemberships": List[str],
        "phiAccessLevel": str,
        "validateData": bool,
        "downloadData": bool,
        "versionView": bool,
    },
)


class UserClaimsContext(ContextBaseModel):
    build_query: bool = Field(alias="buildQuery", default=False)
    can_share: bool = Field(alias="canShare", default=False)
    irb_memberships: List[str] = Field(alias="irbMemberships", default=[])
    phi_access_level: str = Field(alias="phiAccessLevel", default=PhiAccessLevel.NONE)
    validate_data: bool = Field(alias="validateData", default=False)
    download_data: bool = Field(alias="downloadData", default=False)
    version_view: bool = Field(alias="versionView", default=False)

    def context(self) -> UserClaimsTypeDef:
        return cast(
            UserClaimsTypeDef,
            self.dict(by_alias=True),
        )

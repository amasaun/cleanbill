from __future__ import annotations

from typing import List

from src.common.phi_access_level import PhiAccessLevel
from src.models.user_context.user_claims_context import (
    UserClaimsContext,
    UserClaimsTypeDef,
)


class UserClaimsContextBuilder:
    """
    A Builder for a User Context Object.
    """

    _build_query: bool | str
    _can_share: bool | str
    _irb_memberships: List[str]
    _phi_access_level: PhiAccessLevel | str
    _validate_data: bool | str
    _download_data: bool | str
    _version_view: bool | str

    def __init__(self) -> None:
        self._build_query = False
        self._can_share = False
        self._irb_memberships = []
        self._phi_access_level = PhiAccessLevel.NONE
        self._validate_data = False
        self._version_view = False

    def build_query(self, build_query: bool | str) -> UserClaimsContextBuilder:
        self._build_query = build_query
        return self

    def can_share(self, can_share: bool | str) -> UserClaimsContextBuilder:
        self._can_share = can_share
        return self

    def irb_memberships(self, irb_memberships_as_str: str) -> UserClaimsContextBuilder:
        if irb_memberships_as_str == "":
            self._irb_memberships = []
            return self

        self._irb_memberships = irb_memberships_as_str.strip().split(",")
        return self

    def phi_access_level(
        self,
        phi_access_level: PhiAccessLevel | str,
    ) -> UserClaimsContextBuilder:
        self._phi_access_level = phi_access_level
        return self

    def validate_data(self, validate_data: bool | str) -> UserClaimsContextBuilder:
        self._validate_data = validate_data
        return self

    def download_data(self, download_data: bool | str) -> UserClaimsContextBuilder:
        self._download_data = download_data
        return self

    def version_view(self, version_view: bool | str) -> UserClaimsContextBuilder:
        self._version_view = version_view
        return self

    def build(self) -> UserClaimsContext:
        return UserClaimsContext(
            build_query=self._build_query,
            can_share=self._can_share,
            irb_memberships=self._irb_memberships,
            phi_access_level=self._phi_access_level,
            validate_data=self._validate_data,
            download_data=self._download_data,
            version_view=self._version_view,
        )

    def build_dict(self) -> UserClaimsTypeDef:
        return self.build().context()

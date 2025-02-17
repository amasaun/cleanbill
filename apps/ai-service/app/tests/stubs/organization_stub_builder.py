from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4

from src.models.events.organization import Organization


class OrganizationStubBuilder:
    _aws_primary_region: Optional[str]
    _identity_pool_id: Optional[str]
    _uuid: UUID

    def __init__(self) -> None:
        self._aws_primary_region = "us-east-1"
        self._identity_pool_id = "us-east-1_123456789"
        self._uuid = uuid4()

    def aws_primary_region(
        self, aws_primary_region: str | None = None
    ) -> OrganizationStubBuilder:
        self._aws_primary_region = aws_primary_region
        return self

    def identity_pool_id(
        self, identity_pool_id: str | None = None
    ) -> OrganizationStubBuilder:
        self._identity_pool_id = identity_pool_id
        return self

    def uuid(self, uuid: UUID) -> OrganizationStubBuilder:
        self._uuid = uuid
        return self

    def build(self) -> Organization:
        return Organization(
            aws_primary_region=self._aws_primary_region,
            identity_pool_id=self._identity_pool_id,
            uuid=self._uuid,
        )

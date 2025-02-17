from typing import Optional, TypedDict, cast
from uuid import UUID

import simplejson as json
from pydantic import Field

from src.models.events.base_event import BaseEvent


class OrganizationTypeDef(TypedDict):
    aws_primary_region: Optional[str]
    identity_pool_id: Optional[str]
    uuid: str


class Organization(BaseEvent):
    aws_primary_region: Optional[str] = Field(
        alias="awsRegion",
        default=None,
    )
    identity_pool_id: Optional[str] = Field(
        alias="cognitoUserPoolId",
        default=None,
    )
    uuid: UUID = Field(alias="uuid")

    def event_item(self) -> OrganizationTypeDef:
        return cast(
            OrganizationTypeDef,
            json.loads(self.json(by_alias=True)),
        )

from typing import Optional
from uuid import UUID

from src.models.dynamo.base_dynamo_item import BaseDynamoItem, BaseDynamoItemTypeDef


class IDPTypeDef(BaseDynamoItemTypeDef):
    organization_uuid: Optional[str]
    url: str


class IDPItem(
    BaseDynamoItem[IDPTypeDef],
):
    organization_uuid: UUID
    url: str

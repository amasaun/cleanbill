from uuid import UUID

from src.models.dynamo.base_dynamo_item import BaseDynamoItem, BaseDynamoItemTypeDef


class UserTypeDef(BaseDynamoItemTypeDef):
    account_uuid: str
    cognito_user_pool_id: str
    organization_uuid: str
    username: str


class UserItem(
    BaseDynamoItem[UserTypeDef],
):
    account_uuid: UUID
    cognito_user_pool_id: str
    organization_uuid: UUID
    username: str

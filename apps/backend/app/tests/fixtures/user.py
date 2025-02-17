import pytest
from mypy_boto3_dynamodb.service_resource import Table

from src.models.dynamo.user import UserItem
from tests.stubs.user_item_stub_builder import UserItemStubBuilder


@pytest.fixture
def non_persisted_user() -> UserItem:
    return UserItemStubBuilder().build()


@pytest.fixture
def persisted_user(
    idp_table: Table,
    non_persisted_user: UserItem,
) -> UserItem:
    idp_table.put_item(
        Item=non_persisted_user.item(),  # type: ignore[arg-type]
    )
    return non_persisted_user

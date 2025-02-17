import pytest
from mypy_boto3_dynamodb.service_resource import Table

from src.models.dynamo.idp import IDPItem
from tests.stubs.idp_item_stub_builder import IDPItemStubBuilder


@pytest.fixture
def persisted_idp(idp_table: Table) -> IDPItem:
    idp_item = IDPItemStubBuilder().build()
    idp_table.put_item(
        Item=idp_item.item(),  # type: ignore[arg-type]
    )
    return idp_item

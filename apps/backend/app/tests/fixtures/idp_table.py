import os

import boto3
import pytest
from mypy_boto3_dynamodb.service_resource import Table


@pytest.fixture
def idp_table() -> Table:
    table_name = os.environ["IDP_TABLE"]
    return boto3.resource("dynamodb").Table(table_name)

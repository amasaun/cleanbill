import contextlib
import os
from typing import Generator
from uuid import uuid4

import boto3
import moto
import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext

from tests.fixtures import *


@pytest.fixture(scope="function", autouse=True)
def mock_aws_services() -> Generator[None, None, None]:
    with contextlib.ExitStack() as stack:
        mock_services = (moto.mock_dynamodb(),)

        for mock_service in mock_services:
            stack.enter_context(mock_service)

        db_client = boto3.client("dynamodb")

        db_client.create_table(
            BillingMode="PAY_PER_REQUEST",
            TableName=os.environ["IDP_TABLE"],
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
        )

        yield


@pytest.fixture
def mock_context() -> LambdaContext:
    class MockContext(LambdaContext):
        def __init__(self):
            self._function_name = "test"
            self._memory_limit_in_mb = 128
            self._invoked_function_arn = (
                "arn:aws:lambda:us-east-1:12345678:function:test"
            )
            self._aws_request_id = str(uuid4())

    return MockContext()

import os
from functools import cache

import boto3
from mypy_boto3_dynamodb.service_resource import Table


@cache
def idp_table() -> Table:
    return boto3.resource("dynamodb").Table(os.environ["IDP_TABLE"])

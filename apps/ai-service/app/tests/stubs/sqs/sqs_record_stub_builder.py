from __future__ import annotations

from typing import Any, Dict, Literal
from uuid import uuid4

import simplejson as json
from tests.stubs.sqs.sqs_record_attribute_stub_builder import SqsRecordAttributeBuilder

from src.type_defs.sqs import SqsRecordAttributesTypeDef, SqsRecordTypeDef


class SqsRecordStubBuilder:
    _attributes: SqsRecordAttributesTypeDef
    _aws_region: str
    _body: str
    _event_source_arn: str
    _event_source: Literal["aws:sqs"]
    _md5_of_body: str
    _message_attributes: Dict[str, Any]
    _message_id: str
    _receipt_handle: str

    def __init__(self) -> None:
        self._attributes = SqsRecordAttributeBuilder().build()
        self._aws_region = "us-east-1"
        self._body = json.dumps({"key": "value"})
        self._event_source_arn = "arn:aws:sqs:us-east-1:123456789:test-queue"
        self._event_source = "aws:sqs"
        self._md5_of_body = str(uuid4()).replace("-", "")
        self._message_attributes = {}
        self._message_id = str(uuid4())
        self._receipt_handle = str(uuid4()).replace("-", "")

    def attributes(
        self,
        attributes: SqsRecordAttributesTypeDef,
    ) -> SqsRecordStubBuilder:
        self._attributes = attributes
        return self

    def aws_region(self, region: str) -> SqsRecordStubBuilder:
        self._aws_region = region
        return self

    def body(self, body: str) -> SqsRecordStubBuilder:
        self._body = body
        return self

    def event_source_arn(
        self,
        arn: str,
    ) -> SqsRecordStubBuilder:
        self._event_source_arn = arn
        return self

    def event_source(
        self,
        event_source: str,
    ) -> SqsRecordStubBuilder:
        self._event_source = event_source  # type: ignore [assignment]
        return self

    def md5_of_body(
        self,
        md5_of_body: str,
    ) -> SqsRecordStubBuilder:
        self._md5_of_body = md5_of_body
        return self

    def message_attributes(
        self,
        message_attributes: Dict[str, Any],
    ) -> SqsRecordStubBuilder:
        self._message_attributes = message_attributes
        return self

    def message_id(self, message_id: str) -> SqsRecordStubBuilder:
        self._message_id = message_id
        return self

    def receipt_handle(
        self,
        receipt_handle: str,
    ) -> SqsRecordStubBuilder:
        self._receipt_handle = receipt_handle
        return self

    def build(self) -> SqsRecordTypeDef:
        return {
            "attributes": self._attributes,
            "awsRegion": self._aws_region,
            "body": self._body,
            "eventSource": self._event_source,
            "eventSourceARN": self._event_source_arn,
            "md5OfBody": self._md5_of_body,
            "messageAttributes": self._message_attributes,
            "messageId": self._message_id,
            "receiptHandle": self._receipt_handle,
        }

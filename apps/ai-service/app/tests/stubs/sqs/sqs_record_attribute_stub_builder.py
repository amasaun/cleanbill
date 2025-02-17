from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.type_defs.sqs import SqsRecordAttributesTypeDef


class SqsRecordAttributeBuilder:
    _approximate_first_receive_timestamp: str
    _approximate_receive_count: str
    _sender_id: str
    _sent_timestamp: str

    def __init__(self) -> None:
        self._approximate_first_receive_timestamp = str(
            datetime.utcnow().timestamp(),
        )
        self._approximate_receive_count = "1"
        self._sender_id = str(uuid4())
        self._sent_timestamp = str(
            datetime.utcnow().timestamp(),
        )

    def approximate_first_received_timestamp(
        self,
        approximate_first_received_timestamp: datetime,
    ) -> SqsRecordAttributeBuilder:
        self._approximate_first_receive_timestamp = str(
            approximate_first_received_timestamp.timestamp()
        )

        return self

    def approximate_receive_count(
        self,
        approximate_receive_count: int,
    ) -> SqsRecordAttributeBuilder:
        self._approximate_receive_count = str(approximate_receive_count)
        return self

    def sender_id(self, sender_id: str) -> SqsRecordAttributeBuilder:
        self._sender_id = sender_id
        return self

    def sent_timestamp(self, sent_timestamp: datetime) -> SqsRecordAttributeBuilder:
        self._sent_timestamp = str(sent_timestamp.timestamp())
        return self

    def build(self) -> SqsRecordAttributesTypeDef:
        return {
            "ApproximateFirstReceiveTimestamp": self._approximate_first_receive_timestamp,
            "ApproximateReceiveCount": self._approximate_receive_count,
            "SenderId": self._sender_id,
            "SentTimestamp": self._sent_timestamp,
        }

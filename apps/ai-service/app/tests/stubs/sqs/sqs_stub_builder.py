from __future__ import annotations

from typing import List

from tests.stubs.sqs.sqs_record_stub_builder import SqsRecordStubBuilder

from src.type_defs.sqs import SqsRecordsTypeDef, SqsRecordTypeDef


class SqsStubBuilder:
    _records: List[SqsRecordTypeDef]

    def __init__(self):
        self._records = [
            SqsRecordStubBuilder().build(),
        ]

    def records(
        self,
        records: List[SqsRecordTypeDef],
    ) -> SqsStubBuilder:
        self._records = records
        return self

    def build(self) -> SqsRecordsTypeDef:
        return {"Records": self._records}

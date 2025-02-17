from typing import Any, Dict, List, Literal, TypedDict

SqsRecordAttributesTypeDef = TypedDict(
    "SqsRecordAttributesTypeDef",
    {
        "ApproximateFirstReceiveTimestamp": str,
        "ApproximateReceiveCount": str,
        "SenderId": str,
        "SentTimestamp": str,
    },
)


SqsRecordTypeDef = TypedDict(
    "SqsRecordTypeDef",
    {
        "attributes": SqsRecordAttributesTypeDef,
        "awsRegion": str,
        "body": str,
        "eventSource": Literal["aws:sqs"],
        "eventSourceARN": str,
        "md5OfBody": str,
        "messageAttributes": Dict[str, Any],
        "messageId": str,
        "receiptHandle": str,
    },
)

SqsRecordsTypeDef = TypedDict(
    "SqsRecordsTypeDef",
    {
        "Records": List[SqsRecordTypeDef],
    },
)

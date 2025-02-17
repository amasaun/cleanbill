from aws_lambda_powertools.utilities.batch.types import PartialItemFailureResponse

from src.type_defs.sqs import SqsRecordTypeDef


def assert_no_batch_item_failures(
    response: PartialItemFailureResponse,
) -> None:
    assert response == {"batchItemFailures": []}


def assert_record_in_batch_item_failures(
    response: PartialItemFailureResponse,
    record: SqsRecordTypeDef,
) -> None:
    assert {
        "itemIdentifier": record["messageId"],
    } in response["batchItemFailures"]

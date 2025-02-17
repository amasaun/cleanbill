from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    EventType,
    process_partial_response,
)
from aws_lambda_powertools.utilities.batch.types import PartialItemFailureResponse
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import parse_obj_as

from src.common.handler_setup import create_idp_service
from src.common.idp_table import idp_table
from src.common.idp_url_from_identity_id import idp_url_from_identity_id
from src.models.dynamo.idp import IDPItem
from src.models.events.entity_wrapper import EntityWrapper
from src.models.events.organization import Organization
from src.repositories.idp_repository import IDPRepository
from src.type_defs.sqs import SqsRecordsTypeDef

logger = Logger()
sqs_batch_processor = BatchProcessor(event_type=EventType.SQS)

table = idp_table()
idp_service = create_idp_service(table, logger=logger)


def _ingest_organization(record: SQSRecord) -> None:
    data = record.json_body.get("detail", {})
    logger.info(
        "Ingesting Organization",
        extra={
            "organization_uuid": data.get("entity", {}).get("uuid", ""),
        },
    )

    organization_event = parse_obj_as(EntityWrapper[Organization], data)
    organization = organization_event.entity

    if not organization.identity_pool_id or not organization.aws_primary_region:
        logger.warning(
            "Organization Missing Information",
            extra={
                "organization": organization.event_item(),
            },
        )

        raise ValueError("Organization Missing Information")

    url = idp_url_from_identity_id(
        organization.identity_pool_id,
        organization.aws_primary_region,
    )
    item = IDPItem(
        entity=IDPRepository.entity,
        organization_uuid=organization.uuid,
        pk=IDPRepository.pk(url),
        sk=IDPRepository.sk(url),
        url=url,
    )

    idp_service.upsert_idp(item)


@logger.inject_lambda_context
def ingest_organization(
    event: SqsRecordsTypeDef,
    context: LambdaContext,
) -> PartialItemFailureResponse:
    """
    Listens to Organization Events and saves/transforms the event into a
    an IDPItem.
    """
    return process_partial_response(
        event=event,  # type: ignore [arg-type]
        record_handler=_ingest_organization,
        processor=sqs_batch_processor,
        context=context,
    )

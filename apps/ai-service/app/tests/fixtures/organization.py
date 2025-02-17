import pytest
import simplejson as json

from src.models.events.organization import Organization
from src.type_defs.event_bridge import EventBridgeEventTypeDef
from src.type_defs.sqs import SqsRecordsTypeDef, SqsRecordTypeDef
from tests.stubs.events.event_bridge_stub_builder import EventBridgeStubBuilder
from tests.stubs.organization_stub_builder import OrganizationStubBuilder
from tests.stubs.sqs.sqs_record_stub_builder import SqsRecordStubBuilder
from tests.stubs.sqs.sqs_stub_builder import SqsStubBuilder


@pytest.fixture
def organization() -> Organization:
    return OrganizationStubBuilder().build()


@pytest.fixture
def organization_event(organization: Organization) -> EventBridgeEventTypeDef:
    return (
        EventBridgeStubBuilder()
        .detail(
            {"entity": organization.event_item()},
        )
        .build()
    )


@pytest.fixture
def organization_sqs_record(
    organization_event: EventBridgeEventTypeDef,
) -> SqsRecordTypeDef:
    return (
        SqsRecordStubBuilder()
        .body(
            json.dumps(organization_event),
        )
        .build()
    )


@pytest.fixture
def organization_sqs_event(
    organization_sqs_record: SqsRecordTypeDef,
) -> SqsRecordsTypeDef:
    return SqsStubBuilder().records([organization_sqs_record]).build()


@pytest.fixture
def organization_with_missing_information() -> Organization:
    return OrganizationStubBuilder().aws_primary_region().identity_pool_id().build()


@pytest.fixture
def organization_event_with_missing_information(
    organization_with_missing_information: Organization,
) -> EventBridgeEventTypeDef:
    organization = organization_with_missing_information
    return (
        EventBridgeStubBuilder()
        .detail(
            {
                "entity": organization.event_item(),
            }
        )
        .build()
    )


@pytest.fixture
def organization_sqs_record_with_missing_information(
    organization_event_with_missing_information: EventBridgeEventTypeDef,
) -> SqsRecordTypeDef:
    return (
        SqsRecordStubBuilder()
        .body(
            json.dumps(organization_event_with_missing_information),
        )
        .build()
    )


@pytest.fixture
def organization_sqs_event_with_missing_information(
    organization_sqs_record_with_missing_information: SqsRecordTypeDef,
) -> SqsRecordsTypeDef:
    return (
        SqsStubBuilder()
        .records([organization_sqs_record_with_missing_information])
        .build()
    )


@pytest.fixture
def organization_with_missing_region() -> Organization:
    return OrganizationStubBuilder().aws_primary_region().build()


@pytest.fixture
def organization_event_with_missing_region(
    organization_with_missing_region: Organization,
) -> EventBridgeEventTypeDef:
    organization = organization_with_missing_region
    return (
        EventBridgeStubBuilder()
        .detail(
            {"entity": organization.event_item()},
        )
        .build()
    )


@pytest.fixture
def organization_sqs_record_with_missing_region(
    organization_event_with_missing_region: EventBridgeEventTypeDef,
) -> SqsRecordTypeDef:
    return (
        SqsRecordStubBuilder()
        .body(
            json.dumps(organization_event_with_missing_region),
        )
        .build()
    )


@pytest.fixture
def organization_sqs_event_with_missing_region(
    organization_sqs_record_with_missing_region: SqsRecordTypeDef,
) -> SqsRecordsTypeDef:
    return (
        SqsStubBuilder()
        .records(
            [organization_sqs_record_with_missing_region],
        )
        .build()
    )


@pytest.fixture
def organization_with_missing_identity_pool_id() -> Organization:
    return OrganizationStubBuilder().identity_pool_id().build()


@pytest.fixture
def organization_event_with_missing_identity_pool_id(
    organization_with_missing_identity_pool_id: Organization,
) -> EventBridgeEventTypeDef:
    organization = organization_with_missing_identity_pool_id
    return (
        EventBridgeStubBuilder()
        .detail(
            {"entity": organization.event_item()},
        )
        .build()
    )


@pytest.fixture
def organization_sqs_record_with_missing_identity_pool(
    organization_event_with_missing_identity_pool_id: EventBridgeEventTypeDef,
) -> SqsRecordTypeDef:
    return (
        SqsRecordStubBuilder()
        .body(
            json.dumps(organization_event_with_missing_identity_pool_id),
        )
        .build()
    )


@pytest.fixture
def organization_sqs_event_with_missing_identity_pool_id(
    organization_sqs_record_with_missing_identity_pool: SqsRecordTypeDef,
) -> SqsRecordsTypeDef:
    return (
        SqsStubBuilder()
        .records([organization_sqs_record_with_missing_identity_pool])
        .build()
    )


@pytest.fixture
def organization_sqs_event_with_good_and_bad_records(
    organization_sqs_record: SqsRecordTypeDef,
    organization_sqs_record_with_missing_information: SqsRecordTypeDef,
) -> SqsRecordsTypeDef:
    good_record = organization_sqs_record
    bad_record = organization_sqs_record_with_missing_information
    return SqsStubBuilder().records([good_record, bad_record]).build()

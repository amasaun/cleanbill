from decimal import Decimal

import pytest
import simplejson as json
from aws_lambda_powertools.utilities.batch.exceptions import BatchProcessingError
from aws_lambda_powertools.utilities.typing import LambdaContext
from mypy_boto3_dynamodb.service_resource import Table
from pytest_mock import MockerFixture

from src.ingestion.index import idp_service, ingest_organization
from src.models.dynamo.idp import IDPItem
from src.models.events.organization import Organization
from src.type_defs.sqs import SqsRecordsTypeDef, SqsRecordTypeDef
from tests.assertions import (
    assert_no_batch_item_failures,
    assert_record_in_batch_item_failures,
)
from tests.stubs.events.event_bridge_stub_builder import EventBridgeStubBuilder
from tests.stubs.organization_stub_builder import OrganizationStubBuilder
from tests.stubs.sqs.sqs_record_stub_builder import SqsRecordStubBuilder
from tests.stubs.sqs.sqs_stub_builder import SqsStubBuilder


class TestIngestOrganization:
    def _assert_organization_in_idp_table(
        self,
        idp_table: Table,
        organization: Organization,
    ) -> None:
        items = idp_table.scan()
        assert len(items["Items"]) == 1

        item = items["Items"][0]
        expected_url = f"https://cognito-idp.{organization.aws_primary_region}.amazonaws.com/{organization.identity_pool_id}"
        assert item["organization_uuid"] == str(organization.uuid)
        assert item["url"] == expected_url
        assert item["pk"] == f"IDP#{expected_url}"
        assert item["sk"] == f"IDP#{expected_url}"

    def _assert_idp_table_is_empty(self, idp_table: Table) -> None:
        items = idp_table.scan()
        assert items["Items"] == []

    def test_should_ingest_organization_event_successfully(
        self,
        idp_table: Table,
        mock_context: LambdaContext,
        organization_sqs_event: SqsRecordsTypeDef,
        organization: Organization,
    ) -> None:
        self._assert_idp_table_is_empty(idp_table)

        response = ingest_organization(
            organization_sqs_event,
            mock_context,
        )

        self._assert_organization_in_idp_table(idp_table, organization)
        assert_no_batch_item_failures(response)

    def test_should_raise_value_error(
        self,
        idp_table: Table,
        mock_context: LambdaContext,
        organization_sqs_event_with_missing_information: SqsRecordsTypeDef,
    ) -> None:
        with pytest.raises(BatchProcessingError):
            ingest_organization(
                organization_sqs_event_with_missing_information,
                mock_context,
            )

        self._assert_idp_table_is_empty(idp_table)

    def test_should_update_idp_version(
        self,
        persisted_idp: IDPItem,
        mock_context: LambdaContext,
        idp_table: Table,
    ) -> None:
        organization = (
            OrganizationStubBuilder()
            .uuid(
                persisted_idp.organization_uuid,  # type: ignore[arg-type]
            )
            .build()
        )
        event_bridge_event = (
            EventBridgeStubBuilder()
            .detail(
                {
                    "entity": organization.event_item(),
                },
            )
            .build()
        )
        sqs_record = (
            SqsRecordStubBuilder()
            .body(
                json.dumps(event_bridge_event),
            )
            .build()
        )
        sqs_event = SqsStubBuilder().records([sqs_record]).build()

        ingest_organization(sqs_event, mock_context)

        item = idp_table.get_item(Key=persisted_idp.key())  # type: ignore[arg-type]
        assert item["Item"]["version"] == Decimal("2")

    def test_should_call_idp_service(
        self,
        mock_context: LambdaContext,
        mocker: MockerFixture,
        organization_sqs_event: SqsRecordsTypeDef,
    ) -> None:
        spy = mocker.spy(idp_service, "upsert_idp")
        ingest_organization(organization_sqs_event, mock_context)

        spy.assert_called_once()

    def test_should_handle_partial_failure(
        self,
        idp_table: Table,
        mock_context: LambdaContext,
        organization_sqs_event_with_good_and_bad_records: SqsRecordsTypeDef,
        organization_sqs_record_with_missing_information: SqsRecordTypeDef,
        organization: Organization,
    ) -> None:
        self._assert_idp_table_is_empty(idp_table)

        response = ingest_organization(
            organization_sqs_event_with_good_and_bad_records,
            mock_context,
        )

        self._assert_organization_in_idp_table(
            idp_table,
            organization,
        )

        assert_record_in_batch_item_failures(
            response,
            organization_sqs_record_with_missing_information,
        )

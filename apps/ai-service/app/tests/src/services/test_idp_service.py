import os
from uuid import uuid4

import boto3
import pytest
from pytest_mock import MockerFixture

from src.exceptions.idp_exceptions import IDPNotFound
from src.models.dynamo.idp import IDPItem
from src.repositories.idp_repository import IDPRepository
from src.services.idp_service import IDPService
from tests.stubs.idp_item_stub_builder import IDPItemStubBuilder

table = boto3.resource("dynamodb").Table(os.environ["IDP_TABLE"])
idp_repository = IDPRepository(table=table)
service = IDPService(idp_repository)


class TestIDPService:
    class TestGetIDPFromURL:
        def test_should_retrieve_idp_item_from_url(
            self, persisted_idp: IDPItem
        ) -> None:
            retrieved_idp = service.get_idp_by_url(persisted_idp.url)

            assert retrieved_idp == persisted_idp

        def test_should_raise_idp_not_found(self) -> None:
            with pytest.raises(IDPNotFound):
                service.get_idp_by_url(str(uuid4()))

        def test_should_call_repository(
            self,
            persisted_idp: IDPItem,
            mocker: MockerFixture,
        ) -> None:
            spy = mocker.spy(idp_repository, "get_idp_from_url")

            service.get_idp_by_url(persisted_idp.url)

            spy.assert_called_once_with(persisted_idp.url)

    class TestUpsertIDP:
        def test_should_create_new_item(self) -> None:
            builder = IDPItemStubBuilder()
            new_idp = builder.build()

            created_idp = service.upsert_idp(new_idp)

            assert created_idp == builder.version(new_idp.version + 1).build()

        def test_should_call_repository(
            self,
            mocker: MockerFixture,
        ) -> None:
            builder = IDPItemStubBuilder()
            new_idp = builder.build()
            spy = mocker.spy(idp_repository, "upsert_idp")

            service.upsert_idp(new_idp)

            spy.assert_called_once_with(new_idp)

        def test_should_update_existing_item(
            self,
            persisted_idp: IDPItem,
        ) -> None:
            builder = IDPItemStubBuilder()
            new_idp = (
                builder.url(persisted_idp.url)
                .organization_uuid(persisted_idp.organization_uuid)
                .build()
            )

            updated_idp = service.upsert_idp(new_idp)

            assert updated_idp == builder.version(persisted_idp.version + 1).build()

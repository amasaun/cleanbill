import os
from uuid import uuid4

import boto3

from src.models.dynamo.idp import IDPItem
from src.repositories.idp_repository import IDPRepository
from tests.stubs.idp_item_stub_builder import IDPItemStubBuilder

table = boto3.resource("dynamodb").Table(os.environ["IDP_TABLE"])
idp_repository = IDPRepository(table=table)


class TestIDPRepository:
    class TestEntityAttribute:
        def test_should_be_expected(self) -> None:
            IDPRepository.entity == "IDP"

    class TestPK:
        def test_should_calculate_pk(self) -> None:
            url = str(uuid4())
            pk = IDPRepository.pk(url=url.upper())

            assert pk == f"IDP#{url.lower()}"

    class TestSK:
        def test_should_calculate_sk(self) -> None:
            url = str(uuid4())
            pk = IDPRepository.sk(url=url.upper())

            assert pk == f"IDP#{url.lower()}"

    class TestKey:
        def test_should_calculate_key(self) -> None:
            url = str(uuid4())
            key = IDPRepository.key(url.upper())

            assert key == {
                "pk": f"IDP#{url.lower()}",
                "sk": f"IDP#{url.lower()}",
            }

    class TestGetIDPFromUrl:
        def test_should_return_idp(self, persisted_idp: IDPItem) -> None:
            retrieved_item = idp_repository.get_idp_from_url(persisted_idp.url)

            assert retrieved_item == persisted_idp

        def test_should_return_none_if_not_idp(self) -> None:
            retrieved_item = idp_repository.get_idp_from_url(str(uuid4()))

            assert retrieved_item is None

    class TestUpsertIdp:
        def test_should_create_new_idp(self) -> None:
            builder = IDPItemStubBuilder()
            new_idp = builder.build()
            idp_repository.upsert_idp(new_idp)

            retrieved_item = idp_repository.get_idp_from_url(new_idp.url)

            assert retrieved_item == builder.version(new_idp.version + 1).build()

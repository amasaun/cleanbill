from typing import Optional

from aws_lambda_powertools.utilities.parser.pydantic import parse_obj_as

from src.models.dynamo.idp import IDPItem
from src.repositories.single_table_repository import SingleTableRepository
from src.type_defs.dynamo_key import DynamoKey


class IDPRepository(SingleTableRepository):
    entity: str = "IDP"

    @classmethod
    def pk(  # type: ignore [override]
        cls,
        url: str,
    ) -> str:
        return "#".join([cls.entity, url.lower()])

    @classmethod
    def sk(  # type: ignore [override]
        cls,
        url: str,
    ) -> str:
        return cls.pk(url)

    @classmethod
    def key(  # type: ignore [override]
        cls,
        url: str,
    ) -> DynamoKey:
        return {
            "pk": cls.pk(url),
            "sk": cls.sk(
                url,
            ),
        }

    def get_idp_from_url(self, url: str) -> Optional[IDPItem]:
        key = DynamoKey(
            pk=self.pk(url),
            sk=self.sk(url),
        )

        response = self._table.get_item(
            Key=key,  # type: ignore[arg-type]
        )

        if not response.get("Item"):
            return None

        return parse_obj_as(IDPItem, response["Item"])

    def upsert_idp(self, idp_item: IDPItem) -> IDPItem:
        item = idp_item.item()
        response = self._table.update_item(
            Key=idp_item.key(),  # type: ignore[arg-type]
            UpdateExpression=", ".join(
                [
                    "SET #entity = if_not_exists(#entity, :entity)",
                    "#url = if_not_exists(#url, :url)",
                    "#organization_uuid = if_not_exists(#organization_uuid, :organization_uuid)",
                    "#version = if_not_exists(#version, :version) + :inc",
                ],
            ),
            ExpressionAttributeNames={
                "#entity": "entity",
                "#url": "url",
                "#organization_uuid": "organization_uuid",
                "#version": "version",
            },
            ExpressionAttributeValues={
                ":entity": item["entity"],
                ":url": item["url"],
                ":organization_uuid": item["organization_uuid"],
                ":version": item["version"],
                ":inc": 1,
            },
            ReturnValues="ALL_NEW",
        )

        return parse_obj_as(IDPItem, response["Attributes"])

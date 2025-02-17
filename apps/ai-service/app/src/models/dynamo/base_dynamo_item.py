from typing import Generic, TypedDict, TypeVar

import simplejson as json
from aws_lambda_powertools.utilities.parser import BaseModel, Field
from src.type_defs.dynamo_key import DynamoKey


class BaseDynamoItemTypeDef(TypedDict):
    entity: str
    pk: str
    sk: str
    version: int


T = TypeVar(
    "T",
    bound=BaseDynamoItemTypeDef,
)


class BaseDynamoItem(BaseModel, Generic[T]):
    class Config:
        arbitrary_types_allowed: bool = True
        allow_population_by_field_name: bool = True
        use_enum_values: bool = True

    _exclude_none: bool = True
    entity: str
    pk: str
    sk: str
    version: int = Field(default=0)

    def key(self) -> DynamoKey:
        return {
            "pk": self.pk,
            "sk": self.sk,
        }

    def item(self) -> T:
        data = self.json(
            exclude_none=self._exclude_none,
        )

        return json.loads(data)

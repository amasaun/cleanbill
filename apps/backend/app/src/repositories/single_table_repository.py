from abc import ABC, abstractclassmethod, abstractmethod
from typing import Any, Dict, Optional

from mypy_boto3_dynamodb.service_resource import _Table

from src.type_defs.dynamo_key import DynamoKey


class SingleTableRepository(ABC):
    """
    Abstract class the describes the foundation of saving or retrieving a
    specific entity within a DynamoDB Table utilizing Single Table Design.

    Attributes:
        _table (_Table): Describes the boto3 dynamodb Table Resource to use for
            performing queries.

        parent_entity (str | None): String Literal that describes name of an
            entity that should serve as the Parent resource to the entity this
            repository describes.

        entity (str): The name of the Entity the repository will be responsible
            for.
    """

    _table: _Table
    parent_entity: Optional[str] = None
    entity: str

    def __init__(self, table: _Table):
        self._table = table

    @classmethod
    @abstractmethod
    def pk(
        cls,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """
        Describes the parameters and logic the repository will utilize to
        determine an entity's Partition Key value.

        Returns:
            str: Partition Key values should always be of type str.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def sk(
        cls,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """
        Describes the parameters and logic the repository will utilize to
        determine an entity's Sort Key value.

        Returns:
            str: Partition Key values should always be of type str.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def key(
        cls,
        *args: Any,
        **kwargs: Any,
    ) -> DynamoKey:
        """
        Describes the combination of an entity's PK & SK values that make up a
        DynamoDB item's partition key.
        """
        raise NotImplementedError

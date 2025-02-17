from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class EntityWrapper(GenericModel, Generic[T]):
    entity: T

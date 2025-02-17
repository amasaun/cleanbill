from typing import Generic, TypeVar

from aws_lambda_powertools import Logger

T = TypeVar("T")


class BaseService(Generic[T]):
    """
    Describes a Base Service that would access a DDB Repository
    """

    _repository: T
    _logger: Logger

    def __init__(
        self,
        repository: T,
        logger: Logger = Logger(),
    ) -> None:
        self._repository = repository
        self._logger = logger

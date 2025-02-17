from __future__ import annotations

from src.exceptions.idp_exceptions import IDPNotFound
from src.models.dynamo.idp import IDPItem
from src.repositories.idp_repository import IDPRepository
from src.services.base_service import BaseService


class IDPService(
    BaseService[IDPRepository],
):
    def get_idp_by_url(self, url: str) -> IDPItem:
        idp = self._repository.get_idp_from_url(url)

        if idp is None:
            self._logger.error(
                f"IDP URL not found",
                extra={
                    "idp": url,
                },
            )
            raise IDPNotFound

        return idp

    def upsert_idp(self, idp_item: IDPItem) -> IDPItem:
        return self._repository.upsert_idp(idp_item)

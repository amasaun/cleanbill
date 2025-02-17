from __future__ import annotations

import os
from uuid import UUID, uuid4

from src.models.dynamo.idp import IDPItem
from src.repositories.idp_repository import IDPRepository


class IDPItemStubBuilder:
    _entity: str = IDPRepository.entity
    _organization_uuid: UUID
    _url: str
    _version: int

    def __init__(self) -> None:
        self._organization_uuid = uuid4()
        self._url = os.environ["ISSUER_URL"]
        self._version = 1

    def organization_uuid(self, uuid: UUID) -> IDPItemStubBuilder:
        self._organization_uuid = uuid
        return self

    def url(self, url: str) -> IDPItemStubBuilder:
        self._url = url
        return self

    def version(self, version: int) -> IDPItemStubBuilder:
        self._version = version
        return self

    def build(self) -> IDPItem:
        return IDPItem(
            entity=self._entity,
            organization_uuid=self._organization_uuid,
            pk=IDPRepository.pk(self._url),
            sk=IDPRepository.sk(self._url),
            url=self._url,
            version=self._version,
        )

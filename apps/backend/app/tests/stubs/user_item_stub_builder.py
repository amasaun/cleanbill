from __future__ import annotations

from decimal import Decimal
from uuid import UUID, uuid4

from src.models.dynamo.user import UserItem
from src.repositories.user_repository import UserRepository


class UserItemStubBuilder:
    _account_uuid: UUID
    _cognito_user_pool_id: str
    _organization_uuid: UUID
    _username: str
    _version: int | Decimal

    def __init__(self) -> None:
        self._account_uuid = uuid4()
        self._cognito_user_pool_id = "us-east-1_someTestPoolId"
        self._organization_uuid = uuid4()
        self._username = "test"
        self._version = 1

    def account_uuid(self, account_uuid: UUID) -> UserItemStubBuilder:
        self._account_uuid = account_uuid
        return self

    def cognito_user_pool_id(self, cognito_user_pool_id: str) -> UserItemStubBuilder:
        self._cognito_user_pool_id = cognito_user_pool_id
        return self

    def organization_uuid(self, organization_uuid: UUID) -> UserItemStubBuilder:
        self._organization_uuid = organization_uuid
        return self

    def username(self, username: str) -> UserItemStubBuilder:
        self._username = username
        return self

    def version(self, version: int) -> UserItemStubBuilder:
        self._version = version
        return self

    def build(self) -> UserItem:
        return UserItem(
            account_uuid=self._account_uuid,
            cognito_user_pool_id=self._cognito_user_pool_id,
            entity=UserRepository.entity,
            organization_uuid=self._organization_uuid,
            pk=UserRepository.pk(
                self._username,
                cognito_user_pool_id=self._cognito_user_pool_id,
            ),
            sk=UserRepository.sk(
                self._username,
                cognito_user_pool_id=self._cognito_user_pool_id,
            ),
            username=self._username,
        )

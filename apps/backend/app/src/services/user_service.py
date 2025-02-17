from __future__ import annotations

from uuid import UUID

from src.models.dynamo.user import UserItem
from src.repositories.user_repository import UserRepository
from src.services.base_service import BaseService


class UserService(
    BaseService[UserRepository],
):
    def get_user_by_username(
        self,
        username: str,
        cognito_user_pool_id: str,
    ) -> UserItem | None:
        return self._repository.get_user_by_username(
            username,
            cognito_user_pool_id,
        )

    def put_user(self, user_item: UserItem) -> None:
        self._repository.put_user(user_item)

    def create_user(
        self,
        account_uuid: str | UUID,
        organization_uuid: str | UUID,
        username: str,
        cognito_user_pool_id: str,
    ) -> UserItem:
        user_item = UserItem(
            account_uuid=account_uuid,
            cognito_user_pool_id=cognito_user_pool_id,
            entity=UserRepository.entity,
            organization_uuid=organization_uuid,
            pk=self._repository.pk(
                username,
                cognito_user_pool_id,
            ),
            sk=self._repository.sk(
                username,
                cognito_user_pool_id,
            ),
            username=username,
        )
        self.put_user(user_item)

        return user_item

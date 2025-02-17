from aws_lambda_powertools.utilities.parser.pydantic import parse_obj_as

from src.models.dynamo.user import UserItem
from src.repositories.single_table_repository import SingleTableRepository
from src.type_defs.dynamo_key import DynamoKey


class UserRepository(SingleTableRepository):
    entity: str = "USER"

    @classmethod
    def pk(  # type: ignore [override]
        cls,
        username: str,
        cognito_user_pool_id: str,
    ) -> str:
        return "#".join(
            [
                cls.entity,
                username.lower(),
                "USER_POOL",
                cognito_user_pool_id,
            ]
        )

    @classmethod
    def sk(  # type: ignore [override]
        cls,
        username: str,
        cognito_user_pool_id: str,
    ) -> str:
        return cls.pk(
            username,
            cognito_user_pool_id,
        )

    @classmethod
    def key(  # type: ignore [override]
        cls,
        username: str,
        cognito_user_pool_id: str,
    ) -> DynamoKey:
        return {
            "pk": cls.pk(
                username,
                cognito_user_pool_id,
            ),
            "sk": cls.sk(
                username,
                cognito_user_pool_id,
            ),
        }

    def get_user_by_username(
        self,
        username: str,
        cognito_user_pool_id: str,
    ) -> UserItem | None:
        """
        Retrieves a user by their username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            UserItem: The user that was retrieved from the database.

            None: If no user was found with the provided username.

        """
        response = self._table.get_item(
            Key=self.key(
                username,
                cognito_user_pool_id,
            ),  # type: ignore[arg-type]
        )

        if not response.get("Item"):
            return None

        return parse_obj_as(
            UserItem,
            response["Item"],  # type: ignore[arg-type]
        )

    def put_user(self, user_item: UserItem) -> None:
        """
        Puts a user into the database. Overwrites any existing user with the
        same username.

        Args:
            user_item: The user to put into the database.

        """
        self._table.put_item(
            Item=user_item.item(),  # type: ignore[arg-type]
        )

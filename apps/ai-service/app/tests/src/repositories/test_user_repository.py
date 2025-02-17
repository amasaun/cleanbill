import os

import boto3

from src.models.dynamo.user import UserItem
from src.repositories.user_repository import UserRepository
from tests.stubs.user_item_stub_builder import UserItemStubBuilder

table = boto3.resource("dynamodb").Table(os.environ["IDP_TABLE"])
user_repository = UserRepository(table=table)


class TestUserRepository:
    class TestEntityAttribute:
        def test_should_be_expected(self) -> None:
            UserRepository.entity == "USER"

    class TestPK:
        def test_should_calculate_pk(self) -> None:
            username = "test"
            cognito_user_pool_id = "us-east-1_someTestPoolId"
            pk = UserRepository.pk(
                username=username.upper(),
                cognito_user_pool_id=cognito_user_pool_id,
            )

            assert pk == f"USER#{username.lower()}#USER_POOL#{cognito_user_pool_id}"

    class TestSK:
        def test_should_calculate_sk(self) -> None:
            username = "test"
            cognito_user_pool_id = "us-east-1_someTestPoolId"
            pk = UserRepository.sk(
                username=username.upper(),
                cognito_user_pool_id=cognito_user_pool_id,
            )

            assert pk == f"USER#{username.lower()}#USER_POOL#{cognito_user_pool_id}"

    class TestKey:
        def test_should_calculate_key(self) -> None:
            username = "test"
            cognito_user_pool_id = "us-east-1_someTestPoolId"
            key = UserRepository.key(
                username.upper(),
                cognito_user_pool_id=cognito_user_pool_id,
            )

            expected_attribute_value = (
                f"USER#{username.lower()}#USER_POOL#{cognito_user_pool_id}"
            )
            assert key == {
                "pk": expected_attribute_value,
                "sk": expected_attribute_value,
            }

    class TestGetUserByUsername:
        def test_should_get_user_by_username(
            self,
            persisted_user: UserItem,
        ) -> None:
            username = "test"
            cognito_user_pool_id = "us-east-1_someTestPoolId"
            retrieved_user = user_repository.get_user_by_username(
                username,
                cognito_user_pool_id=cognito_user_pool_id,
            )

            assert retrieved_user is not None
            assert retrieved_user == persisted_user

        def test_should_return_none_if_no_user_found(self) -> None:
            username = "test"
            cognito_user_pool_id = "us-east-1_someTestPoolId"
            retrieved_user = user_repository.get_user_by_username(
                username,
                cognito_user_pool_id,
            )

            assert retrieved_user is None

    class TestPutUser:
        def test_should_put_user(self) -> None:
            builder = UserItemStubBuilder()
            new_user = builder.build()
            user_repository.put_user(new_user)

            retrieved_user = user_repository.get_user_by_username(
                new_user.username,
                new_user.cognito_user_pool_id,
            )

            assert retrieved_user is not None
            assert retrieved_user == new_user

import os

import boto3
from pytest_mock import MockerFixture

from src.models.dynamo.user import UserItem
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from tests.stubs.user_item_stub_builder import UserItemStubBuilder

table = boto3.resource("dynamodb").Table(os.environ["IDP_TABLE"])
user_repository = UserRepository(table=table)
service = UserService(user_repository)


class TestUserService:
    class TestGetUserByUsername:
        def test_should_retrieve_user_by_username(
            self, persisted_user: UserItem
        ) -> None:
            retrieved_user = service.get_user_by_username(
                persisted_user.username,
                persisted_user.cognito_user_pool_id,
            )

            assert retrieved_user == persisted_user

        def test_should_return_none_if_no_user_found(self) -> None:
            retrieved_user = service.get_user_by_username(
                username="test",
                cognito_user_pool_id="test",
            )

            assert retrieved_user is None

        def test_should_call_repository(
            self,
            persisted_user: UserItem,
            mocker: MockerFixture,
        ) -> None:
            spy = mocker.spy(user_repository, "get_user_by_username")

            service.get_user_by_username(
                persisted_user.username,
                persisted_user.cognito_user_pool_id,
            )

            spy.assert_called_once_with(
                persisted_user.username,
                persisted_user.cognito_user_pool_id,
            )

    class TestPutUser:
        def test_should_call_repository(self, mocker: MockerFixture) -> None:
            builder = UserItemStubBuilder()
            new_user = builder.build()
            spy = mocker.spy(user_repository, "put_user")

            service.put_user(new_user)

            spy.assert_called_once_with(new_user)

    class TestCreateUser:
        def test_should_create_user(
            self,
            mocker: MockerFixture,
        ) -> None:
            builder = UserItemStubBuilder()
            new_user = builder.build()
            spy = mocker.spy(user_repository, "put_user")

            created_user = service.create_user(
                account_uuid=new_user.account_uuid,
                organization_uuid=new_user.organization_uuid,
                username=new_user.username,
                cognito_user_pool_id=new_user.cognito_user_pool_id,
            )

            spy.assert_called_once_with(new_user)
            assert created_user == new_user

import os
from http import HTTPStatus
from typing import Callable, Tuple
from uuid import uuid4

import pytest
from requests_mock.adapter import _Matcher
from requests_mock.mocker import Mocker

from src.models.dynamo.user import UserItem
from src.models.user_context.user_claims_context import UserClaimsContext
from src.models.user_context.user_context import UserContext
from src.type_defs.decoded_jwts import DecodedAwsIdTokenTypeDef

base_url = os.environ["CENTRAL_API_ENDPOINT"]
auth_user_url = f"{base_url}/auth/user"


@pytest.fixture
def central_api_auth_user_mock(
    non_persisted_user: UserItem,
    requests_mock: Mocker,
) -> Tuple[str, str, _Matcher]:
    account_uuid_as_str = str(non_persisted_user.account_uuid)
    organization_uuid_as_str = str(non_persisted_user.organization_uuid)
    mock = requests_mock.get(
        status_code=HTTPStatus.OK,
        url=auth_user_url,
        json={
            "accountUuid": account_uuid_as_str,
            "organization": {"uuid": organization_uuid_as_str},
        },
    )

    return account_uuid_as_str, organization_uuid_as_str, mock


@pytest.fixture
def central_api_auth_user_403_mock(requests_mock: Mocker) -> _Matcher:
    return requests_mock.get(
        json={"message": "Forbidden"},
        status_code=HTTPStatus.FORBIDDEN,
        url=auth_user_url,
    )


@pytest.fixture
def central_api_auth_user_401_mock(requests_mock: Mocker) -> _Matcher:
    return requests_mock.get(
        json={"message": "Unauthorized"},
        status_code=HTTPStatus.UNAUTHORIZED,
        url=auth_user_url,
    )


@pytest.fixture
def central_api_auth_user_status_mock(
    requests_mock: Mocker,
) -> Callable[[HTTPStatus, str], _Matcher]:
    def _central_api_auth_user_status_mock(
        status_code: HTTPStatus, message: str = ""
    ) -> _Matcher:
        mock = requests_mock.get(
            json={"message": message},
            status_code=status_code,
            url=auth_user_url,
        )
        return mock

    return _central_api_auth_user_status_mock


@pytest.fixture
def user_claims_context(
    decoded_aws_id_token: DecodedAwsIdTokenTypeDef,
) -> UserClaimsContext:
    return UserClaimsContext(
        build_query=decoded_aws_id_token["custom:build_query"],
        can_share=decoded_aws_id_token["custom:can_share"],
        irb_membership=decoded_aws_id_token["custom:irb_memberships"],
        phi_access_level=decoded_aws_id_token["custom:phi_access_level"],
        validate_data=decoded_aws_id_token["custom:validate_data"],
        download_data=decoded_aws_id_token["custom:download_data"],
        version_view=decoded_aws_id_token["custom:version_view"],
    )


@pytest.fixture
def user_context_callable(
    decoded_aws_id_token: DecodedAwsIdTokenTypeDef,
    user_claims_context: UserClaimsContext,
) -> Callable[[str, str, str], UserContext]:
    def _user_context(
        account_uuid_as_str: str,
        organization_uuid_as_str: str,
        cookie: str,
    ) -> UserContext:
        return UserContext(
            account_uuid=account_uuid_as_str,
            cookie=cookie,
            email=decoded_aws_id_token["email"],
            first_name=decoded_aws_id_token["given_name"],
            last_name=decoded_aws_id_token["family_name"],
            organization_uuid=organization_uuid_as_str,
            role=decoded_aws_id_token.get("custom:role", ""),
            user_claims=user_claims_context,
            username=decoded_aws_id_token["cognito:username"],
        )

    return _user_context


@pytest.fixture
def user_context_callable_without_role(
    decoded_aws_id_token_without_role: DecodedAwsIdTokenTypeDef,
    user_claims_context: UserClaimsContext,
) -> Callable[[str, str, str], UserContext]:
    def _user_context(
        account_uuid_as_str: str,
        organization_uuid_as_str: str,
        cookie: str,
    ) -> UserContext:
        return UserContext(
            account_uuid=account_uuid_as_str,
            cookie=cookie,
            email=decoded_aws_id_token_without_role["email"],
            first_name=decoded_aws_id_token_without_role["given_name"],
            last_name=decoded_aws_id_token_without_role["family_name"],
            organization_uuid=organization_uuid_as_str,
            role=decoded_aws_id_token_without_role.get("custom:role", ""),
            user_claims=user_claims_context,
            username=decoded_aws_id_token_without_role["cognito:username"],
        )

    return _user_context

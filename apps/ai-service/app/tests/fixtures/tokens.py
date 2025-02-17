import base64
from typing import Any, Callable, Dict, List, NamedTuple, cast
from unittest.mock import Mock
from uuid import uuid4

import jwt
import pytest
from _pytest.monkeypatch import MonkeyPatch
from Crypto.PublicKey import RSA
from jwt.api_jwt import decode_complete

from src.type_defs.decoded_jwts import (
    DecodedAwsAccessTokenTypeDef,
    DecodedAwsIdTokenTypeDef,
)
from src.type_defs.jwk import JwkResponse
from tests.stubs.token.pre_decoded_access_token_stub_builder import (
    PreDecodedAccessTokenStubBuilder,
)
from tests.stubs.token.pre_decoded_id_token_stub_builder import (
    PreDecodedIdTokenStubBuilder,
)


class RsaKeys(NamedTuple):
    private_key: bytes
    public_key: bytes


class CookieComponents(NamedTuple):
    aws_id_token: str
    aws_access_token: str
    cookie: str
    cookie_list: List[str]


@pytest.fixture
def kid() -> str:
    return str(uuid4())


@pytest.fixture
def rsa_key() -> RSA.RsaKey:
    return RSA.generate(2048)


@pytest.fixture
def rsa_keys(rsa_key: RSA.RsaKey) -> RsaKeys:
    return RsaKeys(
        private_key=rsa_key.export_key(),
        public_key=rsa_key.public_key().export_key(),
    )


@pytest.fixture
def aws_id_token(
    kid: str,
    rsa_keys: RsaKeys,
) -> str:
    payload = PreDecodedIdTokenStubBuilder().build()
    return jwt.encode(
        payload,  # type: ignore [arg-type]
        key=rsa_keys.private_key,
        algorithm="RS256",
        headers={"kid": kid},
    )


@pytest.fixture
def aws_id_token_without_role(kid: str, rsa_keys: RsaKeys) -> str:
    payload = PreDecodedIdTokenStubBuilder().build_without_role()
    return jwt.encode(
        payload,  # type: ignore [arg-type]
        key=rsa_keys.private_key,
        algorithm="RS256",
        headers={"kid": kid},
    )


@pytest.fixture
def aws_access_token(
    aws_id_token: str,
    kid: str,
    rsa_keys: RsaKeys,
) -> str:
    payload = PreDecodedAccessTokenStubBuilder().build()

    return jwt.encode(
        payload,  # type: ignore [arg-type]
        key=rsa_keys.private_key,
        algorithm="RS256",
        headers={"kid": kid},
    )


@pytest.fixture
def aws_access_token_bad_issuer(
    kid: str,
    rsa_keys: RsaKeys,
) -> str:
    payload = PreDecodedAccessTokenStubBuilder().issuer(str(uuid4())).build()

    return jwt.encode(
        payload,  # type: ignore [arg-type]
        key=rsa_keys.private_key,
        algorithm="RS256",
        headers={"kid": kid},
    )


@pytest.fixture
def decoded_aws_id_token(
    aws_id_token: str,
    rsa_keys: RsaKeys,
) -> DecodedAwsIdTokenTypeDef:
    return cast(
        DecodedAwsIdTokenTypeDef,
        jwt.decode(
            aws_id_token,
            rsa_keys.public_key,
            algorithms=["RS256"],
            options={
                "verify_aud": False,
            },
        ),
    )


@pytest.fixture
def decoded_aws_id_token_without_role(
    aws_id_token_without_role: str,
    rsa_keys: RsaKeys,
) -> DecodedAwsIdTokenTypeDef:
    return cast(
        DecodedAwsIdTokenTypeDef,
        jwt.decode(
            aws_id_token_without_role,
            rsa_keys.public_key,
            algorithms=["RS256"],
            options={
                "verify_aud": False,
            },
        ),
    )


@pytest.fixture
def complete_decoded_aws_id_token(
    aws_id_token: str,
    rsa_keys: RsaKeys,
) -> Dict[str, Any]:
    return decode_complete(
        aws_id_token,
        rsa_keys.public_key,
        algorithms=["RS256"],
        options={
            "verify_aud": False,
        },
    )


@pytest.fixture
def decoded_aws_access_token(
    rsa_keys: RsaKeys,
    aws_access_token: str,
) -> DecodedAwsAccessTokenTypeDef:
    return cast(
        DecodedAwsAccessTokenTypeDef,
        jwt.decode(
            aws_access_token,
            key=rsa_keys.public_key,
            algorithms=["RS256"],
            options={
                "verify_aud": False,
            },
        ),
    )


@pytest.fixture
def jwk_response(
    rsa_keys: RsaKeys,
    complete_decoded_aws_id_token: Dict[str, Any],
) -> JwkResponse:
    return {
        "keys": [
            {
                "alg": "RS256",
                "e": "AQAB",
                "kid": complete_decoded_aws_id_token["header"]["kid"],
                "kty": "RSA",
                "n": rsa_keys.public_key.decode("utf-8"),
                "use": "sig",
            }
        ]
    }


@pytest.fixture
def py_jwk_client_mock(
    monkeypatch: MonkeyPatch,
    rsa_keys: RsaKeys,
    complete_decoded_aws_id_token: Dict[str, Any],
) -> Mock:
    jwk_mock = Mock()
    jwk_mock.key = rsa_keys.public_key

    def _signing_key_mock(*args, **kwargs) -> Mock:
        return jwk_mock

    monkeypatch.setattr(
        jwt.jwks_client.PyJWKClient,
        "get_signing_key_from_jwt",
        _signing_key_mock,
    )

    return jwk_mock


@pytest.fixture
def at_hash_patch(
    monkeypatch: MonkeyPatch,
    rsa_keys: RsaKeys,
    complete_decoded_aws_id_token: Dict[str, Any],
) -> Callable[..., None]:
    def _b64_encode_mock(*arg, **kwargs) -> bytes:
        return bytes(
            complete_decoded_aws_id_token["payload"]["at_hash"].encode("utf-8")
        )

    def _patch() -> None:
        monkeypatch.setattr(
            base64,
            "urlsafe_b64encode",
            _b64_encode_mock,
        )

    return _patch


@pytest.fixture
def cookie_components(
    aws_id_token: str,
    aws_access_token: str,
) -> CookieComponents:
    cookie_list = [
        f"awsAccessToken={aws_access_token}",
        f"awsIdToken={aws_id_token}",
    ]
    return CookieComponents(
        aws_access_token=aws_access_token,
        aws_id_token=aws_id_token,
        cookie="; ".join(cookie_list),
        cookie_list=cookie_list,
    )


@pytest.fixture
def cookie_components_without_role(
    aws_id_token_without_role: str,
    aws_access_token: str,
) -> CookieComponents:
    cookie_list = [
        f"awsAccessToken={aws_access_token}",
        f"awsIdToken={aws_id_token_without_role}",
    ]
    return CookieComponents(
        aws_access_token=aws_access_token,
        aws_id_token=aws_id_token_without_role,
        cookie="; ".join(cookie_list),
        cookie_list=cookie_list,
    )

from typing import NamedTuple

from src.type_defs.decoded_jwts import (
    DecodedAwsAccessTokenTypeDef,
    DecodedAwsIdTokenTypeDef,
)


class AwsTokens(NamedTuple):
    access_token: str
    id_token: str


class UnverifiedTokens(NamedTuple):
    access_token: DecodedAwsAccessTokenTypeDef
    id_token: DecodedAwsIdTokenTypeDef


class VerifiedTokens(NamedTuple):
    access_token: str
    id_token: DecodedAwsIdTokenTypeDef

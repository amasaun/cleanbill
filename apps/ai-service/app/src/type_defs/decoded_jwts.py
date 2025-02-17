from __future__ import annotations

from datetime import datetime
from typing import NotRequired, TypeAlias, TypedDict

DecodedAwsAccessTokenTypeDef = TypedDict(
    "DecodedAwsAccessTokenTypeDef",
    {
        "auth_time": int,
        "client_id": str,
        "event_id": str,
        "exp": int,
        "iat": int,
        "iss": str,
        "jti": str,
        "origin_jti": str,
        "scope": str,
        "sub": str,
        "token_use": str,
        "username": str,
        "version": int,
    },
)


DecodedAwsIdTokenTypeDef = TypedDict(
    "DecodedAwsIdTokenTypeDef",
    {
        "at_hash": str,
        "aud": str,
        "auth_time": int,
        "cognito:username": str,
        "custom:auditing_logs": str,
        "custom:build_query": str,
        "custom:can_share": str,
        "custom:download_data": str,
        "custom:irb_memberships": str,
        "custom:phi_access_level": str,
        "custom:role": NotRequired[str],
        "custom:share_recipient": str,
        "custom:tr_access": str,
        "custom:validate_data": str,
        "custom:version_view": str,
        "email": str,
        "event_id": str,
        "exp": int,
        "family_name": str,
        "given_name": str,
        "iat": int,
        "iss": str,
        "jti": str,
        "origin_jti": str,
        "sub": str,
        "token_use": str,
    },
)

TokenDateType: TypeAlias = datetime | int | float


PreDecodedAwsIdTokenTypeDef = TypedDict(
    "PreDecodedAwsIdTokenTypeDef",
    {
        "at_hash": str,
        "aud": str,
        "auth_time": TokenDateType,
        "cognito:username": str,
        "custom:auditing_logs": str,
        "custom:build_query": str,
        "custom:can_share": str,
        "custom:download_data": str,
        "custom:irb_memberships": str,
        "custom:phi_access_level": str,
        "custom:role": NotRequired[str],
        "custom:share_recipient": str,
        "custom:tr_access": str,
        "custom:validate_data": str,
        "custom:version_view": str,
        "email": str,
        "event_id": str,
        "exp": int | datetime,
        "family_name": str,
        "given_name": str,
        "iat": TokenDateType,
        "iss": str,
        "jti": str,
        "origin_jti": str,
        "sub": str,
        "token_use": str,
    },
)


PreDecodedAwsAccessTokenTypeDef = TypedDict(
    "PreDecodedAwsAccessTokenTypeDef",
    {
        "auth_time": TokenDateType,
        "client_id": str,
        "event_id": str,
        "exp": TokenDateType,
        "iat": TokenDateType,
        "iss": str,
        "jti": str,
        "origin_jti": str,
        "scope": str,
        "sub": str,
        "token_use": str,
        "username": str,
        "version": int,
    },
)

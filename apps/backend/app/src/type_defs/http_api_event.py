from __future__ import annotations

from typing import Any, Dict, List, Literal, NotRequired, TypedDict

HttpApiEventHeaders = TypedDict(
    "HttpApiEventHeaders",
    {
        "accept": str,
        "accept-encoding": str,
        "content-length": str,
        "host": NotRequired[str],
        "user-agent": NotRequired[str],
        "x-amzn-trace-id": NotRequired[str],
        "x-forwarded-for": NotRequired[str],
        "x-forwarded-port": NotRequired[str],
        "x-forwarded-proto": NotRequired[str],
    },
)

HttpApiRequestContextLambdaAuthorizerTypeDef = TypedDict(
    "HttpApiRequestContextLambdaAuthorizerTypeDef",
    {
        "lambda": Dict[str, Any],
    },
)

HttpApiRequestContextJwtAttrAuthorizerTypeDef = TypedDict(
    "HttpApiRequestContextJwtAttrAuthorizerTypeDef",
    {
        "claims": Dict[str, str],
        "scopes": List[str],
    },
)

HttpApiRequestContextJwtAuthorizerTypeDef = TypedDict(
    "HttpApiRequestContextJwtAuthorizerTypeDef",
    {
        "jwt": HttpApiRequestContextJwtAttrAuthorizerTypeDef,
    },
)

HttpApiRequestContextHttpTypeDef = TypedDict(
    "HttpApiRequestContextHttpTypeDef",
    {
        "method": Literal[
            "GET",
            "POST",
            "DELETE",
            "PATCH",
            "PUT",
            "OPTIONS",
        ],
        "path": str,
        "protocol": str,
        "sourceIp": str,
        "userAgent": str,
    },
)

HttpApiRequestContextAuthenticationCertValidityTypeDef = TypedDict(
    "HttpApiRequestContextAuthenticationCertValidityTypeDef",
    {
        "notBefore": str,
        "notAfter": str,
    },
)

HttpApiRequestContextAuthenticationClientCertTypeDef = TypedDict(
    "HttpApiRequestContextAuthenticationClientCertTypeDef",
    {
        "clientCertPem": str,
        "subjectDN": str,
        "issuerDN": str,
        "serialNumber": str,
        "validity": HttpApiRequestContextAuthenticationCertValidityTypeDef,
    },
)

HttpApiRequestContextAuthenticationTypeDef = TypedDict(
    "HttpApiRequestContextAuthenticationTypeDef",
    {
        "clientCert": str,
    },
)

HttpApiRequestContextTypeDef = TypedDict(
    "HttpApiRequestContextTypeDef",
    {
        "accountId": str,
        "apiId": str,
        "authentication": NotRequired[HttpApiRequestContextAuthenticationTypeDef],
        "authorizer": HttpApiRequestContextLambdaAuthorizerTypeDef
        | HttpApiRequestContextJwtAuthorizerTypeDef
        | Dict[str, str],
        "domainName": str,
        "domainPrefix": str,
        "http": HttpApiRequestContextHttpTypeDef,
        "requestId": str,
        "routeKey": str,
        "stage": str,
        "time": str,
        "timeEpoch": int,
    },
)

HttpApiEventTypDef = TypedDict(
    "HttpApiEventTypDef",
    {
        "version": Literal["2.0"],
        "routKey": str,
        "rawPath": str,
        "rawQueryString": str,
        "cookies": List[str],
        "headers": HttpApiEventHeaders,
        "queryStringParameters": NotRequired[Dict[str, str]],
        "requestContext": HttpApiRequestContextTypeDef,
        "body": NotRequired[str],
        "pathParameters": NotRequired[Dict[str, str]],
        "isBase64Encoded": bool,
        "stageVariables": NotRequired[Dict[str, str]],
    },
)

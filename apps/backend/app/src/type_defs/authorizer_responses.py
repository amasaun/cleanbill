from typing import Dict, List, Literal, TypedDict

ApiGatewayAuthorizerPolicyStatement = TypedDict(
    "ApiGatewayAuthorizerPolicyStatement",
    {
        "Action": Literal["execute-api:Invoke"],
        "Effect": Literal["Allow", "Deny"],
        "Resource": str,
    },
)

ApiGatewayAuthorizerPolicyDocument = TypedDict(
    "ApiGatewayAuthorizerPolicyDocument",
    {
        "Version": Literal["2012-10-17"],
        "Statement": List[ApiGatewayAuthorizerPolicyStatement],
    },
)

APIGatewayAuthorizerResponseV1TypeDef = TypedDict(
    "APIGatewayAuthorizerResponseV1TypeDef",
    {
        "principalId": str,
        "policyDocument": ApiGatewayAuthorizerPolicyDocument,
        "context": Dict[str, str],
    },
)

APIGatewayAuthorizerResponseV2TypeDef = TypedDict(
    "APIGatewayAuthorizerResponseV2TypeDef",
    {
        "isAuthorized": bool,
        "context": Dict[str, str],
    },
)

from typing import List, Literal, TypedDict

JwkItem = TypedDict(
    "JwkItem",
    {
        "alg": Literal["RS256"],
        "e": Literal["AQAB"],
        "kid": str,
        "kty": Literal["RSA"],
        "n": str,
        "use": Literal["sig"],
    },
)

JwkResponse = TypedDict(
    "JwkResponse",
    {"keys": List[JwkItem]},
)

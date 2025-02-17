from typing import Any, List, Mapping, TypedDict, TypeVar

EventBridgeEventTypeDef = TypedDict(
    "EventBridgeEventTypeDef",
    {
        "account": str,
        "detail-type": str,
        "detail": Mapping[str, Any],
        "id": str,
        "region": str,
        "resources": List[str],
        "source": str,
        "time": str,
        "version": str,
    },
)

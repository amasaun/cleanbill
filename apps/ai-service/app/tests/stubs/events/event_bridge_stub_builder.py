from __future__ import annotations

from datetime import datetime
from typing import Any, List, Literal, Mapping, TypeAlias
from uuid import uuid4

from src.type_defs.event_bridge import EventBridgeEventTypeDef

RegionTypes: TypeAlias = Literal["us-east-1", "us-east-2"]


class EventBridgeStubBuilder:
    _account: str
    _detail_type: str
    _detail: Mapping[str, Any]
    _id: str
    _region: RegionTypes
    _resources: List[str]
    _source: str
    _time: str
    _version: str

    def __init__(self) -> None:
        self._account = "123456789"
        self._detail_type = "ENTITY"
        self._detail = {"key": "value"}
        self._id = str(uuid4())
        self._region = "us-east-1"
        self._resources = []
        self._source = "central-api"
        self._time = datetime.now().isoformat()
        self._version = "0"

    def account(
        self,
        account: str,
    ) -> EventBridgeStubBuilder:
        self._account = account
        return self

    def detail_type(
        self,
        detail_type: str,
    ) -> EventBridgeStubBuilder:
        self._detail_type = detail_type
        return self

    def detail(
        self,
        detail: Mapping[str, Any],
    ) -> EventBridgeStubBuilder:
        self._detail = detail
        return self

    def id(
        self,
        id: str,
    ) -> EventBridgeStubBuilder:
        self._id = id
        return self

    def region(
        self,
        region: RegionTypes,
    ) -> EventBridgeStubBuilder:
        self._region = region
        return self

    def resources(
        self,
        resources: List[str],
    ) -> EventBridgeStubBuilder:
        self._resources = resources
        return self

    def source(
        self,
        source: str,
    ) -> EventBridgeStubBuilder:
        self._source = source
        return self

    def time(self, time: datetime) -> EventBridgeStubBuilder:
        self._time = time.isoformat()
        return self

    def version(
        self,
        version: str,
    ) -> EventBridgeStubBuilder:
        self._version = version
        return self

    def build(self) -> EventBridgeEventTypeDef:
        return {
            "account": self._account,
            "detail-type": self._detail_type,
            "detail": self._detail,
            "id": self._id,
            "region": self._region,
            "resources": self._resources,
            "source": self._source,
            "time": self._time,
            "version": self._version,
        }

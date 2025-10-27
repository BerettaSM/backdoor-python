from typing import Any, Protocol


class Serializer(Protocol):

    def serialize(self, payload: Any) -> bytes: ...

    def deserialize(self, payload: bytes) -> Any: ...

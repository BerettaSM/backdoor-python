from typing import Any, Protocol


class Encoder(Protocol):

    def encode(self, o: Any) -> dict[str, Any]: ...

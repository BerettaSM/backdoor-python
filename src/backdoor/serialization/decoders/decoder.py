from typing import Any, Protocol


class Decoder(Protocol):

    def decode(self, dct: dict[str, Any]) -> Any: ...

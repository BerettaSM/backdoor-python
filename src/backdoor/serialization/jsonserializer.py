import json
from typing import Any

from backdoor.serialization.encoders.commands import CommandEncoder
from backdoor.serialization.decoders.commands import CommandDecoder


class JsonSerializer:

    def serialize(self, payload: Any) -> bytes:
        return json.dumps(payload, cls=CommandEncoder).encode()

    def deserialize(self, data: bytes) -> Any:
        return json.loads(data.decode(), cls=CommandDecoder)

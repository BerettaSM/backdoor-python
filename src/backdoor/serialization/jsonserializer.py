import json
from typing import Any

from backdoor.serialization.decoder import PydanticDecoder
from backdoor.serialization.encoder import PydanticEncoder
from backdoor.serialization.exceptions import BadDataError
from backdoor.serialization.serializer import Serializer


class JsonSerializer(Serializer):

    def serialize(self, payload: Any) -> bytes:
        return json.dumps(payload, cls=PydanticEncoder).encode()

    def deserialize(self, data: bytes) -> Any:
        try:
            return json.loads(data.decode(), cls=PydanticDecoder)
        except json.JSONDecodeError as e:
            raise BadDataError("Data in unexpected format") from e

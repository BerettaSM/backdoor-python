import json
from typing import Any

from backdoor.serialization.encoders.aggregator import EncoderAggregator
from backdoor.serialization.decoders.aggregator import DecoderAggregator
from backdoor.serialization.exceptions import BadDataError


class JsonSerializer:

    def serialize(self, payload: Any) -> bytes:
        return json.dumps(payload, cls=EncoderAggregator).encode()

    def deserialize(self, data: bytes) -> Any:
        try:
            return json.loads(data.decode(), cls=DecoderAggregator)
        except json.JSONDecodeError:
            raise BadDataError("Data in unexpected format")

import json
from typing import Any

from backdoor.serialization.encoders.aggregator import EncoderAggregator
from backdoor.serialization.decoders.aggregator import DecoderAggregator


class JsonSerializer:

    def serialize(self, payload: Any) -> bytes:
        return json.dumps(payload, cls=EncoderAggregator).encode()

    def deserialize(self, data: bytes) -> Any:
        return json.loads(data.decode(), cls=DecoderAggregator)

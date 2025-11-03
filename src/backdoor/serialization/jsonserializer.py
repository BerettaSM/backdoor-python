import json
from typing import Any

from backdoor.serialization.encoders.aggregator import EncoderAggregator
from backdoor.serialization.decoders.aggregator import DecoderAggregator
from backdoor.serialization.exceptions import BadDataError
from backdoor.serialization.serializer import Serializer


class JsonSerializer(Serializer):

    def serialize(self, payload: Any) -> bytes:
        return json.dumps(payload, cls=EncoderAggregator).encode()

    def deserialize(self, data: bytes) -> Any:
        try:
            return json.loads(data.decode(), cls=DecoderAggregator)
        except json.JSONDecodeError as e:
            raise BadDataError("Data in unexpected format") from e

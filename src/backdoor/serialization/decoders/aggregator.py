from json import JSONDecoder
from typing import Any, Sequence

from backdoor.serialization.decoders.commands import CommandDecoder
from backdoor.serialization.decoders.decoder import Decoder
from backdoor.serialization.decoders.exceptions import NotDecodableError


class DecoderAggregator(JSONDecoder):

    decoders: Sequence[Decoder] = (CommandDecoder(),)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(object_hook=self.command_hook, *args, **kwargs)

    def command_hook(self, dct: dict[str, Any]) -> Any | dict[str, Any]:
        for decoder in self.decoders:
            try:
                return decoder.decode(dct)
            except NotDecodableError:
                ...
        return dct

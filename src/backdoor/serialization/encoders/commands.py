from dataclasses import asdict
from typing import Any

from backdoor.models.commands import Command
from backdoor.serialization.encoders.encoder import Encoder
from backdoor.serialization.encoders.exceptions import NotEncodableError


class CommandEncoder(Encoder):

    def encode(self, o: Any) -> Any:
        match o:
            case Command():
                _dict = asdict(o)
                if isinstance(_dict["payload"], bytes):
                    _dict["payload"] = _dict["payload"].decode()
                elif _dict["payload"] is not None:
                    raise ValueError(
                        "Invalid payload type on encoding. Expected: bytes"
                    )
                return _dict
            case _:
                raise NotEncodableError

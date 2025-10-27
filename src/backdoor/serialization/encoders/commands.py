from dataclasses import asdict
from json import JSONEncoder
from typing import Any

from backdoor.models.commands import Command


class CommandEncoder(JSONEncoder):

    def default(self, o: Any) -> Any:
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
                return JSONEncoder.default(self, o)

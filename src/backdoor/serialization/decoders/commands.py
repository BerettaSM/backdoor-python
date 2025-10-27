from json import JSONDecoder
from typing import Any

from backdoor.models.commands import Command


class CommandDecoder(JSONDecoder):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(object_hook=self.command_hook, *args, **kwargs)

    def command_hook(self, dct: dict[str, Any]) -> Command | dict[str, Any]:
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
        return dct

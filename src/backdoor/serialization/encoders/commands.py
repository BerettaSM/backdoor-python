from typing import Any

from backdoor.models.commands import Command
from backdoor.serialization.encoders.encoder import Encoder
from backdoor.serialization.encoders.exceptions import NotEncodableError


class CommandEncoder(Encoder):

    def encode(self, o: Any) -> Any:
        match o:
            case Command():
                return o.model_dump()
            case _:
                raise NotEncodableError

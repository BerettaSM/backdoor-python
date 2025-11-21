from typing import Any

from pydantic import ValidationError

from backdoor.models.commands import RemoteCommand, CommandResult
from backdoor.serialization.decoders.decoder import Decoder
from backdoor.serialization.decoders.exceptions import NotDecodableError


class CommandDecoder(Decoder):

    def decode(self, dct: dict[str, Any]) -> RemoteCommand:
        try:
            return RemoteCommand.model_validate(dct)
        except ValidationError as e:
            err, *_ = e.errors()
            loc, *_ = err.get("loc") or ("Unknown location",)
            msg = err.get("msg") or "Something went wrong"
            raise NotDecodableError(f"{msg} ({loc})")


class CommandResultDecoder(Decoder):

    def decode(self, dct: dict[str, Any]) -> CommandResult:
        try:
            return CommandResult.model_validate(dct)
        except ValidationError as e:
            err, *_ = e.errors()
            loc, *_ = err.get("loc") or ("Unknown location",)
            msg = err.get("msg") or "Something went wrong"
            raise NotDecodableError(f"{msg} ({loc})")

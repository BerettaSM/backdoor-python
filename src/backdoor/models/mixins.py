from typing import Optional

from pydantic import field_serializer


class PayloadSerializerMixin:

    @field_serializer("payload")
    def serialize_payload(self, payload: Optional[bytes]) -> Optional[str]:
        return payload.decode() if payload else None

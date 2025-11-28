from json import JSONEncoder
from typing import Any

from pydantic import BaseModel


class PydanticEncoder(JSONEncoder):

    def default(self, o: Any) -> Any:
        if isinstance(o, BaseModel):
            return o.model_dump()
        return JSONEncoder.default(self, o)

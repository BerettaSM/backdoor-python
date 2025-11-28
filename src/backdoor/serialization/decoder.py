from json import JSONDecoder
from typing import Any, Type, TypeVar

from pydantic import BaseModel, ValidationError


T = TypeVar("T", bound=Type[BaseModel], covariant=True)

registry: list[Type[BaseModel]] = []


def decodable(cls: T) -> T:
    registry.append(cls)
    return cls


class PydanticDecoder(JSONDecoder):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(object_hook=self.command_hook, *args, **kwargs)

    def command_hook(self, dct: dict[str, Any]) -> Any | dict[str, Any]:
        for cls in registry:
            try:
                return cls.model_validate(dct)
            except ValidationError:
                ...
        return dct

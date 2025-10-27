from dataclasses import dataclass
from typing import Optional


@dataclass
class Command:
    command: str
    args: Optional[list[str]] = None
    payload: Optional[bytes] = None

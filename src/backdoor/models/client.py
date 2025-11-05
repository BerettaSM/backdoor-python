from socket import socket
from typing import Optional

from pydantic import BaseModel, ConfigDict

from backdoor.models.systemreport import SystemReport


class ClientModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    host: str
    port: int
    sock: socket
    report: Optional[SystemReport] = None

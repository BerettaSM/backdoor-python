from socket import socket

from pydantic import BaseModel, ConfigDict


class ServerModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    host: str
    port: int
    sock: socket

from socket import socket
from typing import Any

from backdoor.messages.protocol import SocketProtocol
from backdoor.serialization.serializer import Serializer


class SocketMessenger:

    def __init__(self, protocol: SocketProtocol, serializer: Serializer) -> None:
        self.protocol = protocol
        self.serializer = serializer

    def send(self, host: socket, message: Any) -> None:
        payload = self.serializer.serialize(message)
        self.protocol.send(host, payload)

    def receive(self, host: socket) -> Any:
        payload = self.protocol.read(host)
        return self.serializer.deserialize(payload)

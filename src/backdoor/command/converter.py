# pyright: reportUnusedVariable=false
from backdoor.models.commands import Command, LocalCommand, RemoteCommand


LOCAL_COMMANDS = ("systemreport", "help")


class InputToCommandConverter:

    def convert(self, input_: str) -> Command:
        tokens = input_.split(" ")
        command, *args = tokens
        cls = self.__resolve_command_type(command)
        return cls(**locals())

    def __resolve_command_type(self, command: str) -> type[Command]:
        if command in LOCAL_COMMANDS:
            return LocalCommand
        return RemoteCommand

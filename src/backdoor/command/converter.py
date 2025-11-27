# pyright: reportUnusedVariable=false
import re
from backdoor.models.commands import Command, LocalCommand, RemoteCommand


LOCAL_COMMANDS = ("systemreport", "help")

ARGS_REGEX = re.compile(
    r"""
    (?P<unquoted>[^'"\s]+)?             # unquoted word
    \s*                                 # optional space
    ((['"])(?P<quoted>[^\3]*?)\3)?        # everything inside quotes
""",
    re.VERBOSE,
)


class InputToCommandConverter:

    def convert(self, input_: str) -> Command:
        tokens = self.__tokenize_input(input_)
        command, *args = tokens
        cls = self.__resolve_command_type(command)
        return cls(**locals())

    def __resolve_command_type(self, command: str) -> type[Command]:
        if command in LOCAL_COMMANDS:
            return LocalCommand
        return RemoteCommand

    def __tokenize_input(self, input_: str) -> list[str]:
        tokens: list[str] = []
        for match in ARGS_REGEX.finditer(input_):
            unquoted = match.group("unquoted")
            quoted = match.group("quoted")
            if unquoted:
                tokens.append(unquoted)
            if quoted:
                tokens.append(quoted)
        return tokens

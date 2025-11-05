# pyright: reportUnusedVariable=false
from backdoor.models.commands import Command


class InputToCommandConverter:

    def convert(self, input_: str) -> Command:
        tokens = input_.split(" ")
        command, *args = tokens
        return Command(**locals())

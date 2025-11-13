import PyInstaller.__main__
from pathlib import Path


HERE = Path(__file__).parent.absolute()
path_to_server = str(HERE / 'src' / 'backdoor' / 'server.py')
path_to_client = str(HERE / 'src' / 'backdoor' / 'client.py')


def build() -> None:
    PyInstaller.__main__.run([
        path_to_server,
        '--onefile',
        '--windowed',
        '--name', 'server'
    ])

    PyInstaller.__main__.run([
        path_to_client,
        '--onefile',
        '--windowed',
        '--name', 'client'
    ])


if __name__ == '__main__':
    build()

from pathlib import Path


ROOT = Path(__file__).parent.absolute()


def recursive_delete(path: Path) -> None:
    if not path.exists():
        return
    if path.is_file():
        path.unlink()
    else:
        for subpath in path.glob('*'):
            recursive_delete(subpath)
        path.rmdir()


def cleanup() -> None:
    paths = [
        ROOT / '.pytest_cache',
        ROOT / '.mypy_cache',
        ROOT / 'build',
        ROOT / 'dist',
        *ROOT.glob('*.spec')
    ]

    for path in paths:
        recursive_delete(path)


if __name__ == '__main__':
    cleanup()

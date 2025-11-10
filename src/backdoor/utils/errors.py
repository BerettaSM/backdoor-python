import sys


def print_error(err: Exception) -> None:
    sys.stderr.write(str(err) + '\n')
    sys.stderr.flush()

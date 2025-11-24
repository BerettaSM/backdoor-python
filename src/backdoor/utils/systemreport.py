import re
from typing import Any

from backdoor.models.systemreport import SystemReport


THREE_OR_MORE_LINEBREAKS = re.compile(r"\n{3,}")
TWO_LINEBREAKS = "\n" * 2


def format_report(report: SystemReport) -> str:
    return __recursive_format(report.model_dump())


def __recursive_format(report: Any, indent: int = 0) -> str:
    output = ""
    space = indent * " "
    if isinstance(report, dict):
        for key, value in report.items():  # type: ignore
            output += f"{space}{key}: "
            if isinstance(value, dict | list):
                output += "\n"
            output += __recursive_format(value, indent + 1)
        output += f"\n"
    elif isinstance(report, list):
        for item in report:  # type: ignore
            output += __recursive_format(item, indent + 1)
        output += f"\n"
    else:
        output += f"{space}{report}\n"
    return THREE_OR_MORE_LINEBREAKS.sub(TWO_LINEBREAKS, output)

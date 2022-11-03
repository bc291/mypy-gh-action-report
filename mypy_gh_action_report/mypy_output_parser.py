import dataclasses
import re
import sys
from collections import defaultdict
from typing import Any, Literal, Pattern

from mypy_gh_action_report.workflow_command_gen import generate_workflow_commands

LINE_PATTERN: Pattern = re.compile(
    r"(?P<file_name>.*\.py[i]?)" r":(?P<line_no>\d*):\s" r"(?P<type>error|note)" r":\s*" r"(?P<message>.*)"
)


@dataclasses.dataclass
class MypyError:
    file_name: str
    line_no: int
    type: Literal["error", "note"]
    message: str
    error_code: str | None  # TODO: get list of

    def __post_init__(self):
        self.line_no = int(self.line_no)


def __resolve_error_code(error_code_raw: str) -> str | None:
    if not error_code_raw:
        return None

    return error_code_raw[1:-1]


def __resolve_error_line(error_line_raw: str) -> dict[str, Any] | None:
    matched = re.match(LINE_PATTERN, error_line_raw)

    if matched is None:
        return None

    return matched.groupdict()


def parse_mypy_line(mypy_line: str) -> MypyError | None:
    error_line_raw, _, error_code_raw = mypy_line.partition("  ")
    error_code = __resolve_error_code(error_code_raw=error_code_raw)
    error_line = __resolve_error_line(error_line_raw=error_line_raw)

    if error_line is None:
        return None

    return MypyError(**error_line, error_code=error_code)


def convert_mypy_output_to_dict(mypy_output: str) -> defaultdict[str, list[dict[str, Any]]]:
    result = defaultdict(list)

    for mypy_line in mypy_output.splitlines()[:-1]:
        parsed_line = parse_mypy_line(mypy_line=mypy_line.strip())

        result[parsed_line.file_name].append(
            {
                "line_no": parsed_line.line_no,
                "error_code": parsed_line.error_code,
                "type": parsed_line.type,
                "message": parsed_line.message,
            }
        )

    return result


def mypy_to_gh_action_workflow(raw_mypy: str):
    mypy_output_as_dict = convert_mypy_output_to_dict(mypy_output=raw_mypy)
    print(generate_workflow_commands(mypy_output_as_dict=mypy_output_as_dict))


if __name__ == "__main__":
    mypy_to_gh_action_workflow(sys.stdin.read())
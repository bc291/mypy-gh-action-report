import re
from collections import defaultdict
from typing import Any, Dict, Optional, Pattern, Union

from mypy_gh_action_report.models import MypyError
from mypy_gh_action_report.types import MypyErrorsDict

LINE_PATTERN: Pattern = re.compile(
    r"(?P<file_name>.*\.py[i]?)" r":(?P<line_no>\d*):\s" r"(?P<type>error|note)" r":\s*" r"(?P<message>.*)"
)


def __resolve_error_code(error_code_raw: str) -> Optional[str]:
    if not error_code_raw:
        return None

    return error_code_raw[1:-1]


def __resolve_error_line(error_line_raw: str) -> Optional[Dict[str, Any]]:
    matched = re.match(LINE_PATTERN, error_line_raw)

    if matched is None:
        return None

    return matched.groupdict()


def parse_mypy_line(mypy_line: str) -> Optional[MypyError]:
    error_line_raw, _, error_code_raw = mypy_line.partition("  ")
    error_code = __resolve_error_code(error_code_raw=error_code_raw)
    error_line = __resolve_error_line(error_line_raw=error_line_raw)

    if error_line is None:
        return None

    return MypyError(**error_line, error_code=error_code)


def convert_mypy_output_to_dict(mypy_output: str) -> MypyErrorsDict:
    result = defaultdict(list)

    for mypy_line in mypy_output.splitlines()[:-1]:
        parsed_line = parse_mypy_line(mypy_line=mypy_line.strip())

        if not parsed_line:
            continue

        result[parsed_line.file_name].append(
            {
                "line_no": parsed_line.line_no,
                "error_code": parsed_line.error_code,
                "type": parsed_line.type,
                "message": parsed_line.message,
            }
        )

    return dict(**result)

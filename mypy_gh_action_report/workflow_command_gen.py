from typing import DefaultDict

from actions_toolkit import core


def generate_workflow_commands(mypy_output_as_dict: DefaultDict[dict[str, int]]):
    for file, errors in mypy_output_as_dict.items():
        for error in errors:
            core.warning(error["message"], file=file, start_line=error["line_no"])

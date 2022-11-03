from typing import DefaultDict, Dict

from actions_toolkit import core


def generate_workflow_commands(mypy_output_as_dict: DefaultDict):
    for file, errors in mypy_output_as_dict.items():
        for error in errors:
            core.warning(error["message"], file=file, start_line=error["line_no"])

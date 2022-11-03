from collections import defaultdict

from actions_toolkit import core


def generate_workflow_commands(mypy_output_as_dict: defaultdict[dict[str, int]]):
    for file, errors in mypy_output_as_dict.items():
        for error in errors:
            core.warning(error["message"], file=file, start_line=error["line_no"])

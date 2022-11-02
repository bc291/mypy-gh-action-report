from actions_toolkit import core


def generate_workflow_commands(mypy_output_as_dict: dict[dict[str, int]]):
    for file, data in mypy_output_as_dict.items():
        for msg, line_no in data.items():
            core.warning(msg, file=file, start_line=line_no)

import json

from actions_toolkit import core

from mypy_gh_action_report.types import MypyErrorsDict


def get_json_representation(mypy_output: MypyErrorsDict) -> str:
    json_dump = json.dumps(mypy_output)

    return json_dump


def get_workflow_commands(mypy_output: MypyErrorsDict) -> None:
    for file, errors in mypy_output.items():
        for error in errors:
            core.warning(error["message"], file=file, start_line=error["line_no"])

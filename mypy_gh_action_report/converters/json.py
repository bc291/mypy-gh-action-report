import json

from mypy_gh_action_report.types import MypyErrorsDict


def get_json_representation(mypy_output: MypyErrorsDict) -> str:
    return json.dumps(mypy_output)

import dataclasses
import json
from json import JSONEncoder

from mypy_gh_action_report.models import MypyError


class MypyErrorEncoder(JSONEncoder):
    def default(self, obj: MypyError) -> dict:
        return dataclasses.asdict(obj)


def get_json_representation(mypy_errors: list[MypyError]) -> str:
    return json.dumps(mypy_errors, cls=MypyErrorEncoder)

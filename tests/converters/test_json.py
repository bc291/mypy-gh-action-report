import pytest

from mypy_gh_action_report.converters.json import get_json_representation
from mypy_gh_action_report.models import MypyError, MypyErrorType

TEST_DATA_1 = [
    MypyError(
        file_name="file_name.py",
        line_no=1,
        type=MypyErrorType.ERROR,
        message="message",
        error_code="assignment",
    ),
]
TEST_DATA_2 = TEST_DATA_1 + [
    MypyError(
        file_name="file_name2",
        line_no=1,
        type=MypyErrorType.NOTE,
        message="message2",
        error_code=None,
    ),
]


@pytest.mark.parametrize(
    "data, expected",
    (
        (
            TEST_DATA_1,
            '[{"file_name": "file_name.py", "line_no": 1, "type": "error", "message": "message", '
            '"error_code": "assignment"}]',
        ),
        (
            TEST_DATA_2,
            '[{"file_name": "file_name.py", "line_no": 1, "type": "error", "message": "message", '
            '"error_code": "assignment"}, {"file_name": "file_name2", "line_no": 1, "type": "note", '
            '"message": "message2", "error_code": null}]',
        ),
    ),
)
def test_get_json_representation(data, expected):
    # when
    result = get_json_representation(mypy_errors=data)

    # then
    assert result == expected

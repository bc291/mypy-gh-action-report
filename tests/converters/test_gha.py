import pytest

from mypy_gh_action_report.converters.gha import get_workflow_commands
from mypy_gh_action_report.models import MypyError, MypyErrorType


@pytest.fixture
def data():
    return [
        MypyError(
            file_name="app/core/core.py",
            line_no=18,
            error_code="arg-type",
            type=MypyErrorType.ERROR,
            message="Argument 1 to 'test' has incompatible type 'str'; expected 'int'",
        ),
        MypyError(
            file_name="app/models/model.py",
            line_no=53,
            error_code="assignment",
            type=MypyErrorType.ERROR,
            message="Incompatible types in assignment (expression has type 'str', variable has type 'int')",
        ),
        MypyError(
            file_name="app/models/model.py",
            line_no=54,
            error_code="assignment",
            type=MypyErrorType.ERROR,
            message="Incompatible types in assignment (expression has type 'str', variable has type 'int')",
        ),
        MypyError(
            file_name="app/services/service.py",
            line_no=57,
            error_code="assignment",
            type=MypyErrorType.ERROR,
            message=(
                "Incompatible default for argument 'get_data' " "(default has type 'int', argument has type 'str')"
            ),
        ),
        MypyError(
            file_name="app/services/service2/file1.py",
            line_no=66,
            error_code=None,
            type=MypyErrorType.NOTE,
            message="Library stubs not installed for 'redis' (or incompatible with Python 3.10)",
        ),
    ]


def test_output_workflow_command(capsys, data):
    get_workflow_commands(mypy_errors=data)
    stdout_msg = capsys.readouterr().out.splitlines()

    assert len(stdout_msg) == 5

    assert stdout_msg == [
        "::error title=Error code%3A `arg-type`,file=app/core/core.py,line=18::"
        "Argument 1 to 'test' has incompatible type 'str'; expected 'int'",
        "::error title=Error code%3A `assignment`,file=app/models/model.py,line=53::"
        "Incompatible types in assignment (expression has type 'str', variable has type 'int')",
        "::error title=Error code%3A `assignment`,file=app/models/model.py,line=54::"
        "Incompatible types in assignment (expression has type 'str', variable has type 'int')",
        "::error title=Error code%3A `assignment`,file=app/services/service.py,line=57::"
        "Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')",
        "::warning file=app/services/service2/file1.py,line=66::"
        "Library stubs not installed for 'redis' (or incompatible with Python 3.10)",
    ]

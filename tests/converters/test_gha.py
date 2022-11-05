import pytest

from mypy_gh_action_report.converters.gha import get_workflow_commands


@pytest.fixture
def data():
    return {
        "app/core/core.py": [
            {
                "line_no": 18,
                "error_code": "arg-type",
                "type": "error",
                "message": "Argument 1 to 'test' has incompatible type 'str'; expected 'int'",
            }
        ],
        "app/models/model.py": [
            {
                "line_no": 53,
                "error_code": "assignment",
                "type": "error",
                "message": "Incompatible types in assignment (expression has type 'str', variable has type 'int')",
            },
            {
                "line_no": 54,
                "error_code": "assignment",
                "type": "error",
                "message": "Incompatible types in assignment (expression has type 'str', variable has type 'int')",
            },
        ],
        "app/services/service.py": [
            {
                "line_no": 57,
                "error_code": "assignment",
                "type": "error",
                "message": (
                    "Incompatible default for argument 'get_data' " "(default has type 'int', argument has type 'str')"
                ),
            }
        ],
        "app/services/service2/file1.py": [
            {
                "line_no": 66,
                "error_code": None,
                "type": "note",
                "message": "Library stubs not installed for 'redis' (or incompatible with Python 3.10)",
            }
        ],
    }


def test_output_workflow_command(capsys, data):
    get_workflow_commands(mypy_output=data)
    stdout_msg = capsys.readouterr().out.splitlines()

    assert len(stdout_msg) == 5

    assert stdout_msg == [
        "::error title=Mypy found%3A `arg-type`,file=app/core/core.py,line=18,endLine=,col=,endColumn=::"
        "Argument 1 to 'test' has incompatible type 'str'; expected 'int'",
        "::error title=Mypy found%3A `assignment`,file=app/models/model.py,line=53,endLine=,col=,endColumn=::"
        "Incompatible types in assignment (expression has type 'str', variable has type 'int')",
        "::error title=Mypy found%3A `assignment`,file=app/models/model.py,line=54,endLine=,col=,endColumn=::"
        "Incompatible types in assignment (expression has type 'str', variable has type 'int')",
        "::error title=Mypy found%3A `assignment`,file=app/services/service.py,line=57,endLine=,col=,endColumn=::"
        "Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')",
        "::warning title=Mypy found an issue,file=app/services/service2/file1.py,line=66,endLine=,col=,endColumn=::"
        "Library stubs not installed for 'redis' (or incompatible with Python 3.10)",
    ]

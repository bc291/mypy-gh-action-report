import pytest

from mypy_gh_action_report.workflow_command_gen import generate_workflow_commands


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
                "message": "Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')",
            }
        ],
        "app/services/service2/file1.py": [
            {
                "line_no": 66,
                "error_code": "arg-type",
                "type": "error",
                "message": "Argument 'input' to 'get_input' has incompatible type 'int'; expected 'str'",
            }
        ],
    }


def test_output_workflow_command(capsys, data):
    generate_workflow_commands(mypy_output_as_dict=data)
    stdout = capsys.readouterr().out.splitlines()

    assert len(stdout) == 5

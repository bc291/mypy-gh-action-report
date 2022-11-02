import pytest

from mypy_gh_action_report.workflow_command_gen import generate_workflow_commands


@pytest.fixture
def data():
    return {
        "app/core/async_redis.py": {
            'Argument 1 to "test" has incompatible type "str"; expected "int"  [arg-type]': 35,
            'Library stubs not installed for "redis" (or incompatible with Python 3.10)  [import]': 213,
        },
        "app/gateways/sanction_scanner.py": {
            'Incompatible default for argument "search_type" (default has type "int", argument has type "SearchType")  [assignment]': 23
        },
        "app/gateways/sanction_scanner_client.py": {
            'Incompatible default for argument "search_type" (default has type "int", argument has type "SearchType")  [assignment]': 34
        },
        "app/models/sanction_scanner.py": {
            'Incompatible types in assignment (expression has type "int", variable has type "SearchType")  [assignment]': 23
        },
        "app/services/screening_providers/sanction_scanner/requestor.py": {
            'Argument "search_type" to "search_by_name" has incompatible type "int"; expected "SearchType"  [arg-type]': 234
        },
    }


def test_output_workflow_command(capsys, data):
    generate_workflow_commands(mypy_output_as_dict=data)
    stdout = capsys.readouterr().out.splitlines()

    assert len(stdout) == 6

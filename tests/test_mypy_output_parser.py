import dataclasses

import pytest

from mypy_gh_action_report.main import MypyError, convert_mypy_output_to_dict, parse_mypy_line

TEST_DATA_1 = (
    "app/core/core.py:18"
    ": error: "
    "Argument 1 to 'test' has incompatible type 'str'; expected 'int'  "
    "[arg-type]\n"
    "app/models/model.py:53"
    ": error: "
    "Incompatible types in assignment (expression has type 'str', variable has type 'int')  "
    "[assignment]\n"
    "app/services/service.py:57"
    ": error: "
    "Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')  "
    "[assignment]\n"
    "app/services/service2/file1.py:66"
    ": error: "
    "Argument 'input' to 'get_input' has incompatible type 'int'; expected 'str'  "
    "[arg-type]\n"
    "Found 11 errors in 5 file (checked 10 source files)"
)

TEST_DATA_2 = (
    "app/services/service2/file2.py:85"
    ": error: "
    "Argument 'input' to 'get_input' has incompatible type 'int'; expected 'str'  "
    "[arg-type]\n"
    "app/core/core_file.py:1"
    ": error: "
    "Library stubs not installed for 'redis' (or incompatible with Python 3.10)  "
    "[import]\n"
    "app/core/core_file.py:1"
    ": note: "
    "Hint: 'python3 -m pip install types-redis'\n"
    "app/core/core_file2.py:1"
    ": note: "
    "(or run 'mypy --install-types' to install all missing stub packages)\n"
    "app/core/core_file2.py:1"
    ": note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports\n"
    "app/db/repository.py:31:"
    " error: "
    "Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')  "
    "[assignment]\n"
    "Found 11 errors in 5 file (checked 10 source files)"
)


@dataclasses.dataclass
class Scenario:
    mypy_line: str
    expected_mypy_error: MypyError


@pytest.mark.parametrize(
    "scenario",
    (
        Scenario(
            mypy_line=(
                "app/core/core.py:18: error: "
                "Argument 1 to 'test' has incompatible type 'str'; expected 'int'  [arg-type]"
            ),
            expected_mypy_error=MypyError(
                file_name="app/core/core.py",
                line_no=18,
                type="error",
                message="Argument 1 to 'test' has incompatible type 'str'; expected 'int'",
                error_code="arg-type",
            ),
        ),
        Scenario(
            mypy_line=(
                "app/models/model.py:53: error: "
                "Incompatible types in assignment (expression has type 'str', variable has type 'int')  [assignment]"
            ),
            expected_mypy_error=MypyError(
                file_name="app/models/model.py",
                line_no=53,
                type="error",
                message="Incompatible types in assignment (expression has type 'str', variable has type 'int')",
                error_code="assignment",
            ),
        ),
        Scenario(
            mypy_line=(
                "app/services/service.py:57: error: "
                "Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')  "
                "[assignment]"
            ),
            expected_mypy_error=MypyError(
                file_name="app/services/service.py",
                line_no=57,
                type="error",
                message="Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')",
                error_code="assignment",
            ),
        ),
        Scenario(
            mypy_line=(
                "app/services/service2/file1.py:66: error: "
                "Argument 'input' to 'get_input' has incompatible type 'int'; expected 'str'  [arg-type]"
            ),
            expected_mypy_error=MypyError(
                file_name="app/services/service2/file1.py",
                line_no=66,
                type="error",
                message="Argument 'input' to 'get_input' has incompatible type 'int'; expected 'str'",
                error_code="arg-type",
            ),
        ),
        Scenario(
            mypy_line=(
                "app/core/core_file.py:1: error: "
                "Library stubs not installed for 'redis' (or incompatible with Python 3.10)  [import]"
            ),
            expected_mypy_error=MypyError(
                file_name="app/core/core_file.py",
                line_no=1,
                type="error",
                message="Library stubs not installed for 'redis' (or incompatible with Python 3.10)",
                error_code="import",
            ),
        ),
        Scenario(
            mypy_line="app/core/core_file.py:1: note: Hint: 'python3 -m pip install types-redis'",
            expected_mypy_error=MypyError(
                file_name="app/core/core_file.py",
                line_no=1,
                type="note",
                message="Hint: 'python3 -m pip install types-redis'",
                error_code=None,
            ),
        ),
        Scenario(
            mypy_line=(
                "app/core/core_file2.py:1: note: "
                "(or run 'mypy --install-types' to install all missing stub packages)"
            ),
            expected_mypy_error=MypyError(
                file_name="app/core/core_file2.py",
                line_no=1,
                type="note",
                message="(or run 'mypy --install-types' to install all missing stub packages)",
                error_code=None,
            ),
        ),
        Scenario(
            mypy_line=(
                "app/core/core_file2.py:1: note: "
                "See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports"
            ),
            expected_mypy_error=MypyError(
                file_name="app/core/core_file2.py",
                line_no=1,
                type="note",
                message="See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports",
                error_code=None,
            ),
        ),
        Scenario(
            mypy_line=(
                "app/db/repository.py:31: error: "
                "Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')  "
                "[assignment]"
            ),
            expected_mypy_error=MypyError(
                file_name="app/db/repository.py",
                line_no=31,
                type="error",
                message=(
                    "Incompatible default for argument 'get_data' " "(default has type 'int', argument has type 'str')"
                ),
                error_code="assignment",
            ),
        ),
        Scenario(
            mypy_line=(
                "/opt/homebrew/lib/python3.10/site-packages/numpy/__init__.pyi:642: error: "
                "Positional-only parameters are only supported in Python 3.8 and greater"
            ),
            expected_mypy_error=MypyError(
                file_name="/opt/homebrew/lib/python3.10/site-packages/numpy/__init__.pyi",
                line_no=642,
                type="error",
                message=("Positional-only parameters are only supported in Python 3.8 and greater"),
                error_code=None,
            ),
        ),
        Scenario(
            mypy_line=(
                "app/db/repository.py:31: error: Incompatible default for argument 'get_data' "
                "(default has type 'int', argument has type 'str')  [assignment]"
            ),
            expected_mypy_error=MypyError(
                file_name="app/db/repository.py",
                line_no=31,
                type="error",
                message="Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')",
                error_code="assignment",
            ),
        ),
    ),
)
def test_pattern_matching(scenario):
    # when
    result = parse_mypy_line(mypy_line=scenario.mypy_line)

    # then
    assert result == scenario.expected_mypy_error


def test_convert_mypy_output_to_dict__test_data_1():
    result = convert_mypy_output_to_dict(mypy_output=TEST_DATA_1)

    assert result == {
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
            }
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


def test_convert_mypy_output_to_dict__test_data_2():
    result = convert_mypy_output_to_dict(mypy_output=TEST_DATA_2)

    assert result == {
        "app/services/service2/file2.py": [
            {
                "line_no": 85,
                "error_code": "arg-type",
                "type": "error",
                "message": "Argument 'input' to 'get_input' has incompatible type 'int'; expected 'str'",
            }
        ],
        "app/core/core_file.py": [
            {
                "line_no": 1,
                "error_code": "import",
                "type": "error",
                "message": "Library stubs not installed for 'redis' (or incompatible with Python 3.10)",
            },
            {
                "line_no": 1,
                "error_code": None,
                "type": "note",
                "message": "Hint: 'python3 -m pip install types-redis'",
            },
        ],
        "app/core/core_file2.py": [
            {
                "line_no": 1,
                "error_code": None,
                "type": "note",
                "message": "(or run 'mypy --install-types' to install all missing stub packages)",
            },
            {
                "line_no": 1,
                "error_code": None,
                "type": "note",
                "message": "See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports",
            },
        ],
        "app/db/repository.py": [
            {
                "line_no": 31,
                "error_code": "assignment",
                "type": "error",
                "message": "Incompatible default for argument 'get_data' (default has type 'int', argument has type 'str')",
            }
        ],
    }

from unittest.mock import patch

import pytest
import typer

from mypy_gh_action_report import converter, parser
from mypy_gh_action_report.executors import classify_output, handle_output


@pytest.fixture
def mock_convert_mypy_output_to_dict():
    with patch.object(parser, "convert_mypy_output_to_dict") as mock:
        yield mock


@pytest.fixture
def mock_get_workflow_commands():
    with patch.object(converter, "get_workflow_commands") as mock:
        yield mock


@pytest.fixture
def mock_get_json_representation():
    with patch.object(converter, "get_json_representation") as mock:
        yield mock


def test_classify_output__none():
    with pytest.raises(typer.Exit) as exc_info:
        classify_output(mypy_output=None)

    assert exc_info.value.exit_code == 2


def test_classify_output__empty():
    with pytest.raises(typer.Exit) as exc_info:
        classify_output(mypy_output="")

    assert exc_info.value.exit_code == 2


def test_classify_output__success(capsys):
    with pytest.raises(typer.Exit) as exc_info:
        classify_output(mypy_output="Success something, something")

    assert exc_info.value.exit_code == 0

    stdout = capsys.readouterr().out.splitlines()
    assert stdout[0] == "Success. Nothing to be done"


def test_handle_output__json_only_false(mock_convert_mypy_output_to_dict, mock_get_workflow_commands):
    handle_output("{}", json_only=False)
    mock_convert_mypy_output_to_dict.assert_called_once_with(mypy_output="{}")
    mock_get_workflow_commands.assert_called_once_with(mypy_output=mock_convert_mypy_output_to_dict())


def test_handle_output__json_only_true(mock_convert_mypy_output_to_dict, mock_get_json_representation, capsys):
    mock_get_json_representation.return_value = "{}"
    handle_output("{}", json_only=True)
    mock_convert_mypy_output_to_dict.assert_called_once_with(mypy_output="{}")
    mock_get_json_representation.assert_called_once_with(mypy_output=mock_convert_mypy_output_to_dict())

    stdout = capsys.readouterr().out.splitlines()
    assert stdout[0] == "{}"

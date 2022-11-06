import pytest
import typer

from mypy_gh_action_report.main import version_callback


def test_version_callback(capsys):
    with pytest.raises(typer.Exit) as exc_info:
        version_callback(True)

    assert exc_info.value.exit_code == 0

    stdout = capsys.readouterr().out.splitlines()
    assert "." in stdout[0]


def test_version_callback__false():
    result = version_callback(False)

    assert result is None

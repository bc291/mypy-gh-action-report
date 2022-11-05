from typing import Final, Optional

import typer

from mypy_gh_action_report import parser
from mypy_gh_action_report.converters import gha, json

SUCCESS_KEYWORD: Final[str] = "Success"


def classify_output(mypy_output: Optional[str]) -> None:
    if mypy_output is None:
        typer.secho("Please provide stdin data", fg=typer.colors.RED)
        raise typer.Exit(code=2)

    if not mypy_output:
        # Mypy failed
        raise typer.Exit(code=2)

    if SUCCESS_KEYWORD in mypy_output:
        typer.secho("Success. Nothing to be done", fg=typer.colors.GREEN)
        raise typer.Exit(code=0)


def handle_output(mypy_output: str, json_only: bool) -> None:
    mypy_errors = parser.convert_mypy_output_to_model(mypy_output=mypy_output)

    if json_only:
        typer.secho(json.get_json_representation(mypy_errors=mypy_errors), nl=True)
    else:
        gha.get_workflow_commands(mypy_errors=mypy_errors)

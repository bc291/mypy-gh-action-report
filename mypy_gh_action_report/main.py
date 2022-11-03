import sys
from typing import Final, Optional

import typer

from mypy_gh_action_report.executors import classify_output, handle_output

IS_ATTY: Final[bool] = sys.stdin.isatty()


def run(
    mypy_output: Optional[str] = typer.Argument(None if IS_ATTY else sys.stdin.read(), hidden=True),
    json_only: bool = typer.Option(False, help="Just convert mypy output to json"),
) -> None:
    classify_output(mypy_output=mypy_output)
    handle_output(mypy_output=mypy_output, json_only=json_only)
    raise typer.Exit(code=1)


def execute() -> None:
    typer.run(run)

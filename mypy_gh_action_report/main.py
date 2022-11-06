import sys
import typing
from typing import Final, Optional

import typer

from mypy_gh_action_report.executors import classify_output, handle_output

from . import __version__

IS_ATTY: Final[bool] = sys.stdin.isatty()
app: typer.Typer = typer.Typer()


def version_callback(val: bool) -> None:
    if val:
        typer.echo(__version__)
        raise typer.Exit(code=0)

    return None


@app.command()
def run(
    mypy_output: Optional[str] = typer.Argument(None if IS_ATTY else sys.stdin.read(), hidden=True),
    json_only: bool = typer.Option(False, help="Just convert mypy output to json"),
    _: Optional[bool] = typer.Option(None, "-v", "--version", is_eager=True, callback=version_callback),
) -> None:
    classify_output(mypy_output=mypy_output)
    handle_output(mypy_output=typing.cast(str, mypy_output), json_only=json_only)
    raise typer.Exit(code=1)


def execute() -> None:
    app()

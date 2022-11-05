# Welcome to mypy-gh-action-report

Notify Mypy output via [GitHub Workflow Commands](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions)

## Installation

```bash
pip install mypy-gh-action-report
```

## Usage


```bash
mypy . | mypy-gh-action-report
```

or, to generate JSON output

```bash
mypy . | mypy-gh-action-report --json-only
```

## Output

For the following Mypy output:

```bash
mypy_gh_action_report/types.py:3: error: "list" expects 1 type argument, but 2 given  [type-arg]
mypy_gh_action_report/models.py:13: error: Function is missing a return type annotation  [no-untyped-def]
mypy_gh_action_report/parser.py:46: error: Item "None" of "Optional[MypyError]" has no attribute "file_name"  [union-attr]
mypy_gh_action_report/parser.py:48: error: Item "None" of "Optional[MypyError]" has no attribute "line_no"  [union-attr]
mypy_gh_action_report/main.py:16: error: Argument "mypy_output" to "handle_output" has incompatible type "Optional[str]"; expected "str"  [arg-type]
Found 8 errors in 4 files (checked 7 source files)
```

`mypy-gh-action-report` will generate:

```bash
::warning title=,file=mypy_gh_action_report/types.py,line=3,endLine=,col=,endColumn=::"list" expects 1 type argument, but 2 given
::warning title=,file=mypy_gh_action_report/models.py,line=13,endLine=,col=,endColumn=::Function is missing a return type annotation
::warning title=,file=mypy_gh_action_report/parser.py,line=46,endLine=,col=,endColumn=::Item "None" of "Optional[MypyError]" has no attribute "file_name"
::warning title=,file=mypy_gh_action_report/parser.py,line=48,endLine=,col=,endColumn=::Item "None" of "Optional[MypyError]" has no attribute "line_no"
::warning title=,file=mypy_gh_action_report/main.py,line=16,endLine=,col=,endColumn=::Argument "mypy_output" to "handle_output" has incompatible type "Optional[str]"; expected "str"
```

with `--json-only` flag:

```json
[
   {
      "file_name":"mypy_gh_action_report/types.py",
      "line_no":3,
      "error_code":"type-arg",
      "type":"error",
      "message":"\"list\" expects 1 type argument, but 2 given"
   },
   {
      "file_name":"mypy_gh_action_report/models.py",
      "line_no":13,
      "error_code":"no-untyped-def",
      "type":"error",
      "message":"Function is missing a return type annotation"
   },
   {
      "file_name":"mypy_gh_action_report/parser.py",
      "line_no":46,
      "error_code":"union-attr",
      "type":"error",
      "message":"Item \"None\" of \"Optional[MypyError]\" has no attribute \"file_name\""
   },
   {
      "file_name":"mypy_gh_action_report/parser.py",
      "line_no":48,
      "error_code":"union-attr",
      "type":"error",
      "message":"Item \"None\" of \"Optional[MypyError]\" has no attribute \"line_no\""
   },
   {
      "file_name":"mypy_gh_action_report/main.py",
      "line_no":16,
      "error_code":"arg-type",
      "type":"error",
      "message":"Argument \"mypy_output\" to \"handle_output\" has incompatible type \"Optional[str]\"; expected \"str\""
   }
]
```

## Development

In order to contribute to this project you need to have `poetry` installed.

In order to run tests issue:

```bash
poetry install
poetry run pytest tests/
```

## Exit codes

Following Scenarios are covered:

| Description  | Mypy exit code | mypy-gh-action-report exit code |
|--------------|----------|:--------------------------------|
| Success      | 0 | 0                               |
| Issues found | 1 | 1                               |
| Mypy errors  | 2 | 2                               |

## TODO

1. Group warnings for the same line

## Thanks

- [actions-toolkit](https://github.com/yanglbme/actions-toolkit)
- [typer](https://github.com/tiangolo/typer)

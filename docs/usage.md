<div id="help" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="200">
    <span data-ty="input">mypy-gh-action-report --help</span>
    <span data-ty>Usage: mypy-gh-action-report [OPTIONS] [MYPY_OUTPUT]</span>
    <span data-ty></span>
    <span data-ty>Options:</span>
    <span data-ty>  --json-only / --no-json-only    Just convert mypy output to json  [default: no-json-only]</span>
    <span data-ty>  v, --version                   Show version</span>
    <span data-ty>  --help                          Show this message and exit.</span>
</div>

For the following Mypy output:

```bash
mypy_gh_action_report/types.py:3: error: "list" expects 1 type argument, but 2 given  [type-arg]
mypy_gh_action_report/models.py:13: error: Function is missing a return type annotation  [no-untyped-def]
Found 8 errors in 4 files (checked 7 source files)
```

`mypy-gh-action-report` can generate:

<div id="cmd" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="200">
    <span data-ty="input">mypy . | mypy-gh-action-report</span>
    <span data-ty>::warning title=,file=mypy_gh_action_report/types.py,line=3,endLine=,col=,endColumn=::"list" expects 1 type argument, but 2 given</span>
    <span data-ty>::warning title=,file=mypy_gh_action_report/models.py,line=13,endLine=,col=,endColumn=::Function is missing a return type annotation</span>
</div>

or, with `--json-only` flag:

<div id="cmdJson" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="200">
    <span data-ty="input">mypy . | mypy-gh-action-report --json-only</span>
    <span data-ty>[{"file_name": "mypy_gh_action_report/types.py", "line_no": 3, "error_code": "type-arg", "type": "error", "message": "\\"list\\" expects 1 type argument, but 2 given"}, {"file_name": "mypy_gh_action_report/models.py", "line_no": 13, "error_code": "no-untyped-def", "type": "error", "message": "Function is missing a return type annotation"}]</span>
</div>

import sys

from mypy_json_report import produce_errors_report


def output_workflow_command():
    print("::error file=app.js,line=1::Missing semicolon")


if __name__ == "__main__":
    output_workflow_command()

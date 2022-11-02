import sys


def output_workflow_command():
    print("::error file=app.js,line=1::Missing semicolon", file=sys.stderr)
    print("::error file=app.js,line=1::Missing semicolon", file=sys.stderr)


if __name__ == "__main__":
    output_workflow_command()

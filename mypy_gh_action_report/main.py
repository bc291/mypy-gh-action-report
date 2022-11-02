import sys


def output_workflow_command():
    print("::error file=main.js,line=1::Something awful!", file=sys.stderr)


if __name__ == "__main__":
    output_workflow_command()

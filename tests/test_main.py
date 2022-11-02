from mypy_gh_action_report.main import output_workflow_command


def test():
    output_workflow_command()
    assert 1 == 1

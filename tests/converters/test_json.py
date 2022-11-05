from mypy_gh_action_report.converters.json import get_json_representation


def test_get_json_representation():
    # when
    result = get_json_representation({"test": "test"})

    # then
    assert result == '{"test": "test"}'

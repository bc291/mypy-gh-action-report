from typing import Dict, Final, Optional, Union, cast

from mypy_gh_action_report.models import MypyErrorType, WorkflowMessageType
from mypy_gh_action_report.types import MypyErrorsDict

MYPY_MSG_TYPE_TO_GH_WF_MSG_TYPE_MAPPER: Dict[MypyErrorType, WorkflowMessageType] = {
    MypyErrorType.ERROR: WorkflowMessageType.ERROR,
    MypyErrorType.NOTE: WorkflowMessageType.WARNING,
}

TITLE_BEGINNING: Final[str] = "Mypy found"


def get_gh_workflow_type(_type: str) -> WorkflowMessageType:
    return MYPY_MSG_TYPE_TO_GH_WF_MSG_TYPE_MAPPER[_type]


def construct_message_title(error_code: Optional[str]) -> str:
    if error_code:
        return f"{TITLE_BEGINNING}: `{error_code}`"
    return f"{TITLE_BEGINNING} an issue"


def issue_message(error: Dict[str, Union[int, str]], file: str) -> None:
    gh_workflow_msg_type = get_gh_workflow_type(_type=cast(str, error["type"]))
    title = construct_message_title(error_code=error["error_code"])
    gh_workflow_msg_type.handler(error["message"], title=title, file=file, start_line=error["line_no"])


def get_workflow_commands(mypy_output: MypyErrorsDict) -> None:
    for file, errors in mypy_output.items():
        for error in errors:
            issue_message(error=error, file=file)

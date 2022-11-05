from typing import Dict, Final, List, Optional

from mypy_gh_action_report.models import MypyError, MypyErrorType, WorkflowMessageType

MYPY_MSG_TYPE_TO_GH_WF_MSG_TYPE_MAPPER: Dict[MypyErrorType, WorkflowMessageType] = {
    MypyErrorType.ERROR: WorkflowMessageType.ERROR,
    MypyErrorType.NOTE: WorkflowMessageType.WARNING,
}
TITLE_BEGINNING: Final[str] = "Mypy found"


def get_gh_workflow_type(_type: MypyErrorType) -> WorkflowMessageType:
    return MYPY_MSG_TYPE_TO_GH_WF_MSG_TYPE_MAPPER[_type]


def construct_message_title(error_code: Optional[str]) -> str:
    if error_code:
        return f"{TITLE_BEGINNING}: `{error_code}`"
    return f"{TITLE_BEGINNING} an issue"


def issue_message(error: MypyError) -> None:
    gh_workflow_msg_type = get_gh_workflow_type(_type=error.type)
    title = construct_message_title(error_code=error.error_code)
    gh_workflow_msg_type.handler(error.message, title=title, file=error.file_name, start_line=error.line_no)


def get_workflow_commands(mypy_errors: List[MypyError]) -> None:
    for error in mypy_errors:
        issue_message(error=error)

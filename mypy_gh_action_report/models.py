from __future__ import annotations

import dataclasses
import enum
from typing import Callable, Optional

from github_action_utils import error, notice, warning


class MypyErrorType(str, enum.Enum):
    ERROR = "error"
    NOTE = "note"


@dataclasses.dataclass
class MypyError:
    file_name: str
    line_no: int
    type: MypyErrorType
    message: str
    error_code: Optional[str]

    def __post_init__(self) -> None:
        self.line_no = int(self.line_no)


class WorkflowMessageType(str, enum.Enum):
    ERROR = "error", error
    WARNING = "warning", warning
    NOTICE = "notice", notice

    def __new__(cls, value: str, handler: Callable) -> WorkflowMessageType:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._handler = handler  # type: ignore[attr-defined]
        return obj

    @property
    def handler(self) -> Callable:
        return self._handler  # type: ignore[attr-defined]

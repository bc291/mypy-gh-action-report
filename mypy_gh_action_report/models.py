import dataclasses
from typing import Literal, Optional


@dataclasses.dataclass
class MypyError:
    file_name: str
    line_no: int
    type: Literal["error", "note"]
    message: str
    error_code: Optional[str]

    def __post_init__(self) -> None:
        self.line_no = int(self.line_no)

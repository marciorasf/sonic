from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import Enum


@dataclass(frozen=True)
class ErrorWithReason:
    type: "Enum"
    reason: str

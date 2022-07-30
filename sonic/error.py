from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ErrorWithReason:
    type: Enum
    reason: str

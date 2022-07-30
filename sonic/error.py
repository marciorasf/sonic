from dataclasses import dataclass
from enum import Enum


@dataclass
class ErrorWithReason:
    type: Enum
    reason: str

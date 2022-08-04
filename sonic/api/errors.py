from dataclasses import dataclass
from typing import Set


@dataclass(frozen=True)
class MissingFieldsError:
    fields: Set[str]

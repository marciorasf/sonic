from enum import Enum, auto
from typing import TYPE_CHECKING, List, Protocol

from result import Err, Ok, Result

if TYPE_CHECKING:
    from sonic.domain.model import Transaction


class InsertError(Enum):
    Unknown = auto()


class Repository(Protocol):
    async def insert(self, transaction: "Transaction") -> Result[None, InsertError]:
        pass


class FakeRepository:
    def __init__(self) -> None:
        self._error = False
        self._transactions: List["Transaction"] = []

    def with_error(self) -> "FakeRepository":
        """Should be used only on tests!"""
        self._error = True
        return self

    async def insert(self, transaction: "Transaction") -> Result[None, InsertError]:
        if self._error:
            return Err(InsertError.Unknown)

        self._transactions.append(transaction)
        return Ok()

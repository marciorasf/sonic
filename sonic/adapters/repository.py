from typing import TYPE_CHECKING, List, Protocol

from result import Err, Ok, Result

from sonic.errors import UnknownError

if TYPE_CHECKING:
    from sonic.domain.model import Transaction


class Repository(Protocol):
    async def insert(self, transaction: "Transaction") -> Result[None, UnknownError]:
        pass


class FakeRepository:
    def __init__(self) -> None:
        self._error = False
        self._transactions: List["Transaction"] = []

    def with_error(self) -> "FakeRepository":
        """Should be used only on tests!"""
        self._error = True
        return self

    async def insert(self, transaction: "Transaction") -> Result[None, UnknownError]:
        if self._error:
            return Err(
                UnknownError(
                    f"unknown error while persisting transaction: {transaction}"
                )
            )

        self._transactions.append(transaction)
        return Ok()

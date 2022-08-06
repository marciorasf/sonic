from typing import TYPE_CHECKING, List, Optional

from result import Err, Ok, Result

from sonic.errors import UnknownError
from sonic.service_layer.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from sonic.domain.model import Transaction, TransactionId


class FakeRepository:
    def __init__(self) -> None:
        self._error = False
        self._transactions: List["Transaction"] = []

    def with_error(self) -> "FakeRepository":
        """Should be used only on tests!"""
        self._error = True
        return self

    async def add(self, transaction: "Transaction") -> Result[None, UnknownError]:
        if self._error:
            return Err(
                UnknownError(
                    f"unknown error while persisting transaction: {transaction}"
                )
            )

        self._transactions.append(transaction)
        return Ok()

    async def fetch(
        self, id: "TransactionId"
    ) -> Result[Optional["Transaction"], UnknownError]:
        if self._error:
            return Err(
                UnknownError(f"unknown error while fetching transaction with {id=}")
            )

        t = [t for t in self._transactions if t.id == id]
        if len(t) == 0:
            return Ok(None)

        return Ok(t[0])


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, with_error: bool = False) -> None:
        self.transactions = FakeRepository()
        if with_error:
            self.transactions = self.transactions.with_error()

        self.committed = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass

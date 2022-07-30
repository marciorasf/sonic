from enum import Enum, auto
from typing import List, Protocol

from result import Err, Ok, Result

from sonic.domain.model import Transaction
from sonic.logging import logger


class InsertError(Enum):
    Unknown = auto()


class Repository(Protocol):
    async def insert(self, transaction: Transaction) -> Result[None, InsertError]:
        pass


class InMemoryRepository:
    def __init__(self) -> None:
        self._error = False
        self._transactions: List[Transaction] = []

    def with_error(self) -> "InMemoryRepository":
        """Should be used only on tests!"""
        self._error = True
        return self

    async def insert(self, transaction: Transaction) -> Result[None, InsertError]:
        if self._error:
            return Err(InsertError.Unknown)

        self._transactions.append(transaction)
        logger.debug("Inserted transaction", transaction=transaction)
        return Ok()

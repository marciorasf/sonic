from enum import Enum, auto
from typing import List, Protocol

from result import Ok, Result

from sonic.domain.model import Transaction


class InsertError(Enum):
    Unknown = auto()


class Repository(Protocol):
    async def insert(self, transaction: Transaction) -> Result[None, InsertError]:
        pass


class InMemoryRepository:
    def __init__(self) -> None:
        self._transactions: List[Transaction] = []

    async def insert(self, transaction: Transaction) -> Result[None, InsertError]:
        self._transactions.append(transaction)
        return Ok()

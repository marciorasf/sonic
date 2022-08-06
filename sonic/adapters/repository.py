from typing import TYPE_CHECKING, Optional, Protocol

if TYPE_CHECKING:
    from result import Result

    from sonic.domain.model import Transaction, TransactionId
    from sonic.errors import UnknownError


class Repository(Protocol):
    async def add(self, transaction: "Transaction") -> "Result[None, UnknownError]":
        pass

    async def fetch(
        self, id: "TransactionId"
    ) -> "Result[Optional[Transaction], UnknownError]":
        pass

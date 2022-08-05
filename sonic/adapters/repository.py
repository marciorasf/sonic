from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from result import Result

    from sonic.domain.model import Transaction
    from sonic.errors import UnknownError


class Repository(Protocol):
    async def add(self, transaction: "Transaction") -> "Result[None, UnknownError]":
        pass

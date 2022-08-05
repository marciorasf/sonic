from abc import ABC, abstractmethod

from sonic.adapters.repository import Repository


class UnitOfWork(ABC):
    transactions: Repository

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self) -> None:
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

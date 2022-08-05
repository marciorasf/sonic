from typing import TypeVar

T = TypeVar("T", bound=Exception)


def chain_exc(new_exc: T, cause: Exception) -> T:
    new_exc.__cause__ = cause
    return new_exc


class UnknownError(Exception):
    pass

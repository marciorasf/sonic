from uuid import UUID, uuid4

import pytest


def unreachable() -> None:
    pytest.fail("Unreachable")


def random_transaction_id() -> UUID:
    return uuid4()

import pytest


def unreachable() -> None:
    pytest.fail("Unreachable")

from datetime import datetime
from decimal import Decimal

from result import Err, Ok

from sonic.domain.model import (
    Transaction,
    new_transaction,
    to_client_id,
    to_transaction_description,
    to_transaction_ts,
    to_transaction_value,
)
from tests.helpers import unreachable


def test_to_client_id() -> None:
    res = to_client_id("success")
    match res:
        case Ok(client_id):
            assert client_id == "success"
        case _:
            unreachable()

    res = to_client_id("")
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


def test_to_transaction_ts() -> None:
    res = to_transaction_ts("2021-03-03T03:03:03.300000")
    match res:
        case Ok(t):
            assert t == datetime(2021, 3, 3, 3, 3, 3, 300000)
        case _:
            unreachable()

    res = to_transaction_ts("2021-03-03 03:03:03.300000")
    match res:
        case Ok(t):
            assert t == datetime(2021, 3, 3, 3, 3, 3, 300000)
        case _:
            unreachable()

    res = to_transaction_ts("invalid")
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


def test_to_transaction_value() -> None:
    res = to_transaction_value("20.00")
    match res:
        case Ok(v):
            assert v == Decimal(20)
        case _:
            unreachable()

    res = to_transaction_value("20")
    match res:
        case Ok(v):
            assert v == Decimal(20)
        case _:
            unreachable()

    res = to_transaction_value("20,00")
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()

    res = to_transaction_value("")
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()

    res = to_transaction_value(1e12)
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()

    res = to_transaction_value(-1e12)
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


def test_to_transaction_description() -> None:
    res = to_transaction_description("my_description")
    match res:
        case Ok(d):
            assert d == "my_description"
        case _:
            unreachable()

    res = to_transaction_description("")
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()

    res = to_transaction_description("x" * 1000)
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


def test_new_transaction() -> None:
    res = new_transaction(
        "test_client", "2021-03-03T03:03:03.300000", "20", "description"
    )
    match res:
        case Ok(t):
            assert t == Transaction(
                client_id="test_client",  # type: ignore
                timestamp=datetime(2021, 3, 3, 3, 3, 3, 300000),  # type: ignore
                value=Decimal(20),  # type: ignore
                description="description",  # type: ignore
            )
        case _:
            unreachable()

    res = new_transaction(
        "test_client", "2021-03-03T03:03:03.300000", "", "description"
    )
    match res:
        case Err([ValueError()]):
            pass
        case _:
            unreachable()

    res = new_transaction("test_client", "2021-03-03T03:03:03.300000", "", "")
    match res:
        case Err([ValueError(), ValueError()]):
            pass
        case _:
            unreachable()

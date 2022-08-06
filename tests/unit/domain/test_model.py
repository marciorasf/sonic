from datetime import datetime
from decimal import Decimal
from typing import Any, Callable

from result import Err, Ok

from sonic.domain.model import (
    Transaction,
    new_transaction,
    to_client_id,
    to_transaction_description,
    to_transaction_ts,
    to_transaction_value,
)
from tests.helpers import random_transaction_id, unreachable


def test_to_client_id_happy_path() -> None:
    res = to_client_id("success")
    match res:
        case Ok(client_id):
            assert client_id == "success"
        case _:
            unreachable()


def test_should_return_value_error_when_client_id_is_empty() -> None:
    res = to_client_id("")
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


def test_to_transaction_ts_happy_path() -> None:
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


def test_should_return_value_error_when_timestamp_is_invalid() -> None:
    res = to_transaction_ts("invalid")
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


def test_to_transaction_value_happy_path() -> None:
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


def test_should_return_value_error_when_value_is_invalid() -> None:
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


def test_should_return_value_error_when_value_is_out_of_bounds() -> None:
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


def test_to_description_happy_path() -> None:
    res = to_transaction_description("my_description")
    match res:
        case Ok(d):
            assert d == "my_description"
        case _:
            unreachable()


def test_should_return_value_error_when_description_is_empty() -> None:
    res = to_transaction_description("")
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


def test_should_return_value_error_when_description_is_too_long() -> None:
    res = to_transaction_description("x" * 1000)
    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


def test_new_transaction_happy_path() -> None:
    id = random_transaction_id()

    res = new_transaction(
        id,
        "test_client",
        "2021-03-03T03:03:03.300000",
        "20",
        "description",
    )

    match res:
        case Ok(t):
            assert t == Transaction(
                id=id,
                client_id="test_client",  # type: ignore
                timestamp=datetime(2021, 3, 3, 3, 3, 3, 300000),  # type: ignore
                value=Decimal(20),  # type: ignore
                description="description",  # type: ignore
            )
        case _:
            unreachable()


def test_bench_new_transaction(benchmark: Callable[..., Any]) -> None:
    id = random_transaction_id()

    benchmark(
        new_transaction, id, "test_client", "2021-03-03T03:03:03.300000", "200", "desc"
    )


def test_should_return_value_error_when_invalid_fields_are_provided() -> None:
    res = new_transaction(
        random_transaction_id(),
        "test_client",
        "2021-03-03T03:03:03.300000",
        "",
        "description",
    )
    match res:
        case Err([ValueError()]):
            pass
        case _:
            unreachable()

    res = new_transaction(
        random_transaction_id(), "test_client", "2021-03-03T03:03:03.300000", "", ""
    )
    match res:
        case Err([ValueError(), ValueError()]):
            pass
        case _:
            unreachable()


def test_equality_between_transactions_depends_only_on_id() -> None:
    id = random_transaction_id()
    ts = "2021-03-03T03:03:03.300000"
    v = "20"
    d = "description"

    t1 = new_transaction(id, "client_1", ts, v, d)
    t2 = new_transaction(id, "client_2", ts, v, d)
    t3 = new_transaction(random_transaction_id(), "client_3", ts, v, d)

    assert t1 == t2
    assert t1 != t3

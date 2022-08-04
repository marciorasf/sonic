from datetime import datetime
from decimal import Decimal

from sonic.domain.model import (
    ClientIdError,
    Transaction,
    TransactionDescriptionError,
    TransactionTsError,
    TransactionValueError,
    new_transaction,
    to_client_id,
    to_transaction_description,
    to_transaction_ts,
    to_transaction_value,
)


def test_to_client_id() -> None:
    res = to_client_id("success")
    assert res.is_ok()
    assert res.ok() == "success"

    res = to_client_id("")
    assert res.is_err()
    assert res.err() == ClientIdError.Empty


def test_to_transaction_ts() -> None:
    res = to_transaction_ts("2021-03-03T03:03:03.300000")
    assert res.is_ok()
    assert res.ok() == datetime(2021, 3, 3, 3, 3, 3, 300000)

    res = to_transaction_ts("2021-03-03 03:03:03.300000")
    assert res.is_ok()
    assert res.ok() == datetime(2021, 3, 3, 3, 3, 3, 300000)

    res = to_transaction_ts("invalid")
    assert res.is_err()
    assert res.err() == TransactionTsError.Invalid


def test_to_transaction_value() -> None:
    res = to_transaction_value("20.00")
    assert res.is_ok()
    assert res.ok() == Decimal(20)

    res = to_transaction_value("20")
    assert res.is_ok()
    assert res.ok() == Decimal(20)

    res = to_transaction_value("20,00")
    assert res.is_err()
    assert res.err() == TransactionValueError.Invalid

    res = to_transaction_value("")
    assert res.is_err()
    assert res.err() == TransactionValueError.Invalid

    res = to_transaction_value(1e12)
    assert res.is_err()
    assert res.err() == TransactionValueError.OutOfBounds

    res = to_transaction_value(-1e12)
    assert res.is_err()
    assert res.err() == TransactionValueError.OutOfBounds


def test_to_transaction_description() -> None:
    res = to_transaction_description("my_description")
    assert res.is_ok()
    assert res.ok() == "my_description"

    res = to_transaction_description("")
    assert res.is_err()
    assert res.err() == TransactionDescriptionError.Empty

    res = to_transaction_description("x" * 1000)
    assert res.is_err()
    assert res.err() == TransactionDescriptionError.OutOfBounds


def test_new_transaction() -> None:
    res = new_transaction(
        "test_client", "2021-03-03T03:03:03.300000", "20", "description"
    )
    assert res.is_ok()
    assert res.ok() == Transaction(
        client_id="test_client",  # type: ignore
        timestamp=datetime(2021, 3, 3, 3, 3, 3, 300000),  # type: ignore
        value=Decimal(20),  # type: ignore
        description="description",  # type: ignore
    )

    res = new_transaction(
        "test_client", "2021-03-03T03:03:03.300000", "", "description"
    )
    assert res.is_err()
    assert res.err() == [TransactionValueError.Invalid]

    res = new_transaction("test_client", "2021-03-03T03:03:03.300000", "", "")
    assert res.is_err()
    assert res.err() == [
        TransactionValueError.Invalid,
        TransactionDescriptionError.Empty,
    ]

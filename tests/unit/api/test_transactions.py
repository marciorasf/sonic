import pytest
from result import Err, Ok

from sonic.api.transactions import parse_transaction


def test_parse_transaction_happy_path() -> None:
    t = "client_id=abc-client-1;transaction_timestamp=2022-07-15T03:40:23.123;value=23.10;description=Chocolate store"

    res = parse_transaction(t)

    match res:
        case Ok(req):
            assert req.client_id == "abc-client-1"
            assert req.timestamp == "2022-07-15T03:40:23.123"
            assert req.value == "23.10"
            assert req.description == "Chocolate store"
        case _:
            pytest.fail("Unreachable")


def test_parse_transaction_missing_field() -> None:
    t = "clint_id=abc-client-1;transaction=2022-07-15T03:40:23.123;value=23.10;description=Chocolate store"

    res = parse_transaction(t)

    match res:
        case Err(err):
            assert err.fields == {"client_id", "transaction_timestamp"}
        case _:
            pytest.fail("Unreachable")

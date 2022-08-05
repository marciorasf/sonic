from datetime import datetime
from decimal import Decimal

import pytest
from result import Err, Ok

from sonic.errors import UnknownError
from sonic.service_layer.services import AddTransactionRequest, add_transaction
from tests.fakes import FakeRepository


@pytest.mark.asyncio()
async def test_add_transaction_happy_path() -> None:
    repo = FakeRepository()
    req = AddTransactionRequest(
        client_id="test_client",
        timestamp="2021-03-03T03:03:03.300000",
        value="200.00",
        description="My description",
    )

    res = await add_transaction(repo, req)

    match res:
        case Ok():
            pass
        case _:
            pytest.fail("Unreachable")

    new_transaction = repo._transactions[0]
    assert new_transaction.client_id == "test_client"
    assert new_transaction.timestamp == datetime(2021, 3, 3, 3, 3, 3, 300000)
    assert new_transaction.value == Decimal(200)
    assert new_transaction.description == "My description"


@pytest.mark.asyncio()
async def test_add_transaction_invalid_request() -> None:
    repo = FakeRepository()
    req = AddTransactionRequest(
        client_id="test_client",
        timestamp="2021-03-03T03:03:03.300000",
        value="200.00",
        description="",
    )

    res = await add_transaction(repo, req)

    match res:
        case Err(ValueError()):
            pass
        case _:
            pytest.fail("Unreachable")


@pytest.mark.asyncio()
async def test_add_transaction_unknown_error_on_repo() -> None:
    repo = FakeRepository().with_error()
    req = AddTransactionRequest(
        client_id="test_client",
        timestamp="2021-03-03T03:03:03.300000",
        value="200.00",
        description="My description",
    )

    res = await add_transaction(repo, req)

    match res:
        case Err(UnknownError()):
            pass
        case _:
            pytest.fail("Unreachable")

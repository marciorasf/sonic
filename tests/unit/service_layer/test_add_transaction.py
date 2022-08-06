from datetime import datetime
from decimal import Decimal

import pytest
from result import Err, Ok

from sonic.errors import UnknownError
from sonic.service_layer.services import AddTransactionRequest, add_transaction
from tests.fakes import FakeUnitOfWork
from tests.helpers import unreachable


@pytest.mark.asyncio()
async def test_should_add_transaction() -> None:
    uow = FakeUnitOfWork()
    req = AddTransactionRequest(
        client_id="test_client",
        timestamp="2021-03-03T03:03:03.300000",
        value="200.00",
        description="My description",
    )

    res = await add_transaction(req, uow)

    match res:
        case Ok():
            pass
        case _:
            unreachable()

    new_transaction = uow.transactions._transactions[0]  # type: ignore
    assert new_transaction.client_id == "test_client"
    assert new_transaction.timestamp == datetime(2021, 3, 3, 3, 3, 3, 300000)
    assert new_transaction.value == Decimal(200)
    assert new_transaction.description == "My description"


@pytest.mark.asyncio()
async def test_should_return_value_error_when_the_request_is_invalid() -> None:
    uow = FakeUnitOfWork()
    req = AddTransactionRequest(
        client_id="test_client",
        timestamp="2021-03-03T03:03:03.300000",
        value="200.00",
        description="",
    )

    res = await add_transaction(req, uow)

    match res:
        case Err(ValueError()):
            pass
        case _:
            unreachable()


@pytest.mark.asyncio()
async def test_should_return_unknown_error_when_an_unknown_error_happens() -> None:
    uow = FakeUnitOfWork(with_error=True)
    req = AddTransactionRequest(
        client_id="test_client",
        timestamp="2021-03-03T03:03:03.300000",
        value="200.00",
        description="My description",
    )

    res = await add_transaction(req, uow)

    match res:
        case Err(UnknownError()):
            pass
        case _:
            unreachable()

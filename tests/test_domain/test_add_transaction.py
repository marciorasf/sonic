from result import Ok

from sonic.domain import add_transaction


def test_should_return_ok() -> None:
    req = add_transaction.Request(
        client_id="test_client",
        timestamp="2021-03-03T03:03:03.3Z",
        value="200.00",
        description="My description",
    )

    res = add_transaction.execute(req)

    assert isinstance(res, Ok)

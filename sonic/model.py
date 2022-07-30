from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import NewType

ClientId = NewType("ClientId", str)


def to_client_id(id: str) -> ClientId:
    return ClientId(id)


TransactionTs = NewType("TransactionTs", datetime)


def to_transaction_ts(ts: str) -> TransactionTs:
    return TransactionTs(datetime.fromisoformat(ts))


TransactionValue = NewType("TransactionValue", Decimal)


def to_transaction_value(v: str) -> TransactionValue:
    return TransactionValue(Decimal(v))


TransactionDescription = NewType("TransactionValue", str)


def to_transaction_description(d: str) -> TransactionDescription:
    return TransactionDescription(d)


@dataclass
class Transaction:
    client_id: ClientId
    timestamp: TransactionTs
    value: TransactionValue
    description: TransactionDescription


def new_transaction(
    client_id: str, timestamp: str, value: str, description: str
) -> Transaction:
    return Transaction(
        client_id=to_client_id(client_id),
        timestamp=to_transaction_ts(timestamp),
        value=to_transaction_value(value),
        description=to_transaction_description(description),
    )

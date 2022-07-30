from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import List, NewType

from result import Err, Ok, Result

ClientId = NewType("ClientId", str)


class ClientIdError(Enum):
    Empty = auto()


def to_client_id(id: str) -> Result[ClientId, ClientIdError]:
    if len(id) == 0:
        return Err(ClientIdError.Empty)

    return Ok(ClientId(id))


TransactionTs = NewType("TransactionTs", datetime)


class TransactionTsError(Enum):
    Invalid = auto()


def to_transaction_ts(ts: str) -> Result[TransactionTs, TransactionTsError]:
    try:
        return Ok(TransactionTs(datetime.fromisoformat(ts)))
    except Exception:
        return Err(TransactionTsError.Invalid)


TransactionValue = NewType("TransactionValue", Decimal)


class TransactionValueError(Enum):
    Invalid = auto()
    OutOfBounds = auto()


def to_transaction_value(
    v: str | int | float,
) -> Result[TransactionValue, TransactionValueError]:
    try:
        d = Decimal(v)

        if d > 1e9 or d < -1e9:
            return Err(TransactionValueError.OutOfBounds)

        return Ok(TransactionValue(d))
    except Exception:
        return Err(TransactionValueError.Invalid)


TransactionDescription = NewType("TransactionDescription", str)


class TransactionDescriptionError(Enum):
    Empty = auto()
    OutOfBounds = auto()


def to_transaction_description(
    d: str,
) -> Result[TransactionDescription, TransactionDescriptionError]:
    if len(d) == 0:
        return Err(TransactionDescriptionError.Empty)

    if len(d) > 255:
        return Err(TransactionDescriptionError.OutOfBounds)

    return Ok(TransactionDescription(d))


@dataclass(frozen=True)
class Transaction:
    client_id: ClientId
    timestamp: TransactionTs
    value: TransactionValue
    description: TransactionDescription


NewTransactionError = List[
    ClientIdError
    | TransactionTsError
    | TransactionValueError
    | TransactionDescriptionError
]


def new_transaction(
    client_id: str, timestamp: str, value: str, description: str
) -> Result[Transaction, NewTransactionError]:
    match (
        to_client_id(client_id),
        to_transaction_ts(timestamp),
        to_transaction_value(value),
        to_transaction_description(description),
    ):
        case (Ok(id), Ok(ts), Ok(v), Ok(d)):
            return Ok(
                Transaction(
                    client_id=id,
                    timestamp=ts,
                    value=v,
                    description=d,
                )
            )
        case (id, ts, v, d):
            errors: NewTransactionError = []
            if id.is_err():
                errors.append(id.unwrap_err())

            if ts.is_err():
                errors.append(ts.unwrap_err())

            if v.is_err():
                errors.append(v.unwrap_err())

            if d.is_err():
                errors.append(d.unwrap_err())

            return Err(errors)
        case _:
            raise RuntimeError(
                f"Unknown error while creating transaction: {client_id=}, {timestamp=}, {value=}, {description=}"
            )

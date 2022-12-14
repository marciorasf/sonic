from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, NewType
from uuid import UUID

from result import Err, Ok, Result

from sonic.errors import chain_exc

TransactionId = UUID

ClientId = NewType("ClientId", str)


def to_client_id(id: str) -> Result[ClientId, ValueError]:
    if len(id) == 0:
        return Err(ValueError("client id cannot be empty"))

    return Ok(ClientId(id))


TransactionTs = NewType("TransactionTs", datetime)


def to_transaction_ts(ts: str) -> Result[TransactionTs, ValueError]:
    try:
        return Ok(TransactionTs(datetime.fromisoformat(ts)))
    except Exception as err:
        return Err(chain_exc(ValueError(f"invalid transaction timestamp: {ts}"), err))


TransactionValue = NewType("TransactionValue", Decimal)


def to_transaction_value(
    v: str | int | float,
) -> Result[TransactionValue, ValueError]:
    try:
        d = Decimal(v)

        if d > 1e9 or d < -1e9:
            return Err(ValueError(f"value must be in [-1e9, 1e9], and was {v}"))

        return Ok(TransactionValue(d))
    except Exception as err:
        return Err(
            chain_exc(ValueError(f"value cannot be represented as decimal: {v}"), err)
        )


TransactionDescription = NewType("TransactionDescription", str)


def to_transaction_description(
    d: str,
) -> Result[TransactionDescription, ValueError]:
    if len(d) == 0:
        return Err(ValueError("description cannot be empty"))

    if len(d) > 256:
        return Err(
            ValueError(
                f"description must have less than 256 characters, and {d} has {len(d)} characters"
            )
        )

    return Ok(TransactionDescription(d))


@dataclass(frozen=True, eq=False)
class Transaction:
    id: TransactionId
    client_id: ClientId
    timestamp: TransactionTs
    value: TransactionValue
    description: TransactionDescription

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return False

        return self.id == other.id


def new_transaction(id: UUID, client_id: str, timestamp: str, value: str, description: str) -> Result[Transaction, List[ValueError]]:  # type: ignore[return]
    match (
        to_client_id(client_id),
        to_transaction_ts(timestamp),
        to_transaction_value(value),
        to_transaction_description(description),
    ):
        case (Ok(c_id), Ok(ts), Ok(v), Ok(d)):
            return Ok(
                Transaction(
                    id=id,
                    client_id=c_id,
                    timestamp=ts,
                    value=v,
                    description=d,
                )
            )
        case (c_id, ts, v, d):
            errors: List[ValueError] = []
            if c_id.is_err():
                errors.append(c_id.unwrap_err())

            if ts.is_err():
                errors.append(ts.unwrap_err())

            if v.is_err():
                errors.append(v.unwrap_err())

            if d.is_err():
                errors.append(d.unwrap_err())

            return Err(errors)

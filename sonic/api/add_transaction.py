from dataclasses import dataclass
from typing import Any, Set

from fastapi import APIRouter, HTTPException, status
from result import Err, Ok, Result

from sonic.domain import add_transaction
from sonic.error import ErrorWithReason
from sonic.repositories.transaction import InMemoryRepository

router = APIRouter()


@dataclass
class Request:
    transaction: str


repo = InMemoryRepository()


@router.post("/")
async def serve(req: Request) -> Any:
    match parse_transaction(req.transaction):
        case Ok(t):
            match await add_transaction.execute(repo, t):
                case Ok():
                    return None
                case Err(ErrorWithReason(add_transaction.ErrorType.BadRequest, reason)):
                    raise HTTPException(status.HTTP_400_BAD_REQUEST, reason)
                case Err():
                    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        case Err(MissingFieldsError(reason)):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, reason)


@dataclass(frozen=True)
class MissingFieldsError:
    fields: Set[str]


def parse_transaction(t: str) -> Result[add_transaction.Request, MissingFieldsError]:
    pairs = t.split(";")
    hashmap = {}

    for pair in pairs:
        key, value = pair.split("=")
        hashmap[key] = value

    missing_fields = {
        "client_id",
        "transaction_timestamp",
        "value",
        "description",
    } - hashmap.keys()

    if len(missing_fields):
        return Err(MissingFieldsError(missing_fields))

    return Ok(
        add_transaction.Request(
            client_id=hashmap["client_id"],
            timestamp=hashmap["transaction_timestamp"],
            value=hashmap["value"],
            description=hashmap["description"],
        )
    )

from dataclasses import dataclass
from typing import Dict, Set

from fastapi import APIRouter
from result import Err, Ok, Result

from sonic.domain import add_transaction

router = APIRouter()


@dataclass
class Request:
    transaction: str


@router.post("/")
def serve(req: Request) -> Dict[str, str]:
    return {"Hello": "World"}


@dataclass
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

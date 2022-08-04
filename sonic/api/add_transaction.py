from dataclasses import dataclass
from typing import Set

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from result import Err, Ok, Result

from sonic.adapters.repository import Repository
from sonic.api.shared import get_repo
from sonic.domain import add_transaction
from sonic.error import ErrorWithReason

router = APIRouter()


class Request(BaseModel):
    transaction: str

    class Config:
        schema_extra = {
            "example": {
                "transaction": "client_id=abc-client-1;transaction_timestamp=2022-07-15T03:40:23.123;value=23.10;description=Chocolate store",
            }
        }


repo_dependency = Depends(get_repo)


@router.post("/")
async def serve(req: Request, repo: Repository = repo_dependency) -> None:
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

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from result import Err, Ok, Result

from sonic.adapters.repository import Repository
from sonic.api.dependencies import get_repo
from sonic.api.errors import MissingFieldsError
from sonic.service_layer import services
from tests.fakes import FakeUnitOfWork

router = APIRouter()

repo_dependency = Depends(get_repo)


class AddTransactionReq(BaseModel):
    transaction: str

    class Config:
        schema_extra = {
            "example": {
                "transaction": "client_id=abc-client-1;transaction_timestamp=2022-07-15T03:40:23.123;value=23.10;description=Chocolate store",
            }
        }


@router.post("/")
async def add_transaction(
    req: AddTransactionReq, repo: Repository = repo_dependency
) -> None:
    match parse_transaction(req.transaction):
        case Ok(t):
            match await services.add_transaction(t, FakeUnitOfWork()):
                case Ok():
                    return None
                case Err(ValueError() as err):
                    raise HTTPException(status.HTTP_400_BAD_REQUEST, err)
                case Err():
                    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        case Err(MissingFieldsError(reason)):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, reason)


def parse_transaction(
    t: str,
) -> Result[services.AddTransactionRequest, MissingFieldsError]:
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
        services.AddTransactionRequest(
            client_id=hashmap["client_id"],
            timestamp=hashmap["transaction_timestamp"],
            value=hashmap["value"],
            description=hashmap["description"],
        )
    )

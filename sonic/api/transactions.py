from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from result import Err, Ok, Result

from sonic.api.errors import MissingFieldsError
from sonic.service_layer import services
from tests.fakes import FakeUnitOfWork

router = APIRouter()


class AddTransactionReq(BaseModel):
    transaction: str

    class Config:
        schema_extra = {
            "example": {
                "transaction": "client_id=abc-client-1;transaction_timestamp=2022-07-15T03:40:23.123;value=23.10;description=Chocolate store",
            }
        }


class AddTransactionRes(BaseModel):
    id: UUID

    class Config:
        schema_extra = {"example": {"id": "e5ac89eb-d573-45ed-bc88-0a8f36655a53"}}


@router.post("/", response_model=AddTransactionRes)
async def add_transaction(req: AddTransactionReq) -> AddTransactionRes:  # type: ignore[return]
    match parse_transaction(req.transaction):
        case Ok(t):
            match await services.add_transaction(t, FakeUnitOfWork()):
                case Ok(res):
                    return AddTransactionRes(id=res.id)
                case Err(ValueError() as err):
                    raise HTTPException(status.HTTP_400_BAD_REQUEST, err)
                case Err(err):
                    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, err)
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

from dataclasses import dataclass

from result import Err, Ok, Result

from sonic.domain.model import new_transaction
from sonic.errors import UnknownError
from sonic.service_layer.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class AddTransactionRequest:
    client_id: str
    timestamp: str
    value: str
    description: str


@dataclass
class AddTransactionResponse:
    pass


async def add_transaction(req: AddTransactionRequest, uow: UnitOfWork) -> Result[AddTransactionResponse, ValueError | UnknownError]:  # type: ignore[return]
    match new_transaction(req.client_id, req.timestamp, req.value, req.description):
        case Ok(transaction):
            with uow:
                match (await uow.transactions.add(transaction)):
                    case Ok():
                        uow.commit()
                        return Ok(AddTransactionResponse())
                    case Err(UnknownError() as err):
                        return Err(err)
        case Err(err):
            return Err(ValueError(f"invalid request: {err}"))

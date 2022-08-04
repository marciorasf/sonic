from dataclasses import dataclass
from typing import TYPE_CHECKING

from result import Err, Ok, Result

from sonic.domain.model import new_transaction
from sonic.service_layer.errors import UnknownError

if TYPE_CHECKING:
    from sonic.adapters.repository import Repository


@dataclass(frozen=True)
class AddTransactionRequest:
    client_id: str
    timestamp: str
    value: str
    description: str


@dataclass
class AddTransactionResponse:
    pass


async def add_transaction(repo: "Repository", req: AddTransactionRequest) -> Result[AddTransactionResponse, UnknownError | ValueError]:  # type: ignore[return]
    match new_transaction(req.client_id, req.timestamp, req.value, req.description):
        case Ok(transaction):
            match await repo.insert(transaction):
                case Ok():
                    return Ok(AddTransactionResponse())
                case Err():
                    return Err(UnknownError("error while inserting on repo"))
        case Err(err):
            return Err(ValueError(f"invalid request: {err}"))

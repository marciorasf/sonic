from dataclasses import dataclass
from typing import TYPE_CHECKING

from result import Err, Ok, Result

from sonic.domain.model import new_transaction
from sonic.service_layer.error import UnknownError

if TYPE_CHECKING:
    from sonic.adapters.repository import Repository


@dataclass(frozen=True)
class Request:
    client_id: str
    timestamp: str
    value: str
    description: str


@dataclass
class Response:
    pass


async def add_transaction(repo: "Repository", req: Request) -> Result[Response, UnknownError | ValueError]:  # type: ignore[return]
    match new_transaction(req.client_id, req.timestamp, req.value, req.description):
        case Ok(transaction):
            match await repo.insert(transaction):
                case Ok():
                    return Ok(Response())
                case Err():
                    return Err(UnknownError("error while inserting on repo"))
        case Err(err):
            return Err(ValueError(f"invalid request: {err}"))

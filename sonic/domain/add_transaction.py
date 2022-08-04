from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

from result import Err, Ok, Result

from sonic.domain.model import new_transaction
from sonic.error import ErrorWithReason

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


class ErrorType(Enum):
    BadRequest = auto()
    Unknown = auto()


async def execute(repo: "Repository", req: Request) -> Result[Response, ErrorWithReason]:  # type: ignore[return]
    match new_transaction(req.client_id, req.timestamp, req.value, req.description):
        case Ok(transaction):
            match await repo.insert(transaction):
                case Ok():
                    return Ok(Response())
                case Err():
                    return Err(
                        ErrorWithReason(
                            type=ErrorType.Unknown,
                            reason="error while inserting on repo",
                        )
                    )
        case Err(err):
            return Err(ErrorWithReason(type=ErrorType.BadRequest, reason=err))

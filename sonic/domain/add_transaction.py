from dataclasses import dataclass
from enum import Enum, auto

from result import Err, Ok, Result

from sonic.domain.model import new_transaction
from sonic.logging import logger
from sonic.repositories.transaction import Repository


@dataclass(frozen=True)
class Request:
    client_id: str
    timestamp: str
    value: str
    description: str


@dataclass
class Response:
    pass


class Error(Enum):
    BadRequest = auto()
    Unknown = auto()


async def execute(repo: Repository, req: Request) -> Result[Response, Error]:  # type: ignore[return]
    match new_transaction(req.client_id, req.timestamp, req.value, req.description):
        case Ok(transaction):
            match await repo.insert(transaction):
                case Ok():
                    return Ok(Response())
                case Err():
                    return Err(Error.Unknown)
        case Err(err):
            logger.debug(err)
            return Err(Error.BadRequest)

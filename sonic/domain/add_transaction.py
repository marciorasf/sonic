from dataclasses import dataclass
from enum import Enum, auto

from result import Ok, Result


@dataclass
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


def execute(req: Request) -> Result[Response, Error]:
    return Ok(Response())

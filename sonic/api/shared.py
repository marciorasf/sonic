from typing import TYPE_CHECKING, cast

from fastapi import Request

if TYPE_CHECKING:
    from sonic.repositories.transaction import Repository


def get_repo(request: Request) -> "Repository":
    return cast("Repository", request.state.repo)

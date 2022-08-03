from fastapi import APIRouter

from sonic.api import add_transaction

router = APIRouter()

router.include_router(
    add_transaction.router, prefix="/transactions", tags=["transactions"]
)

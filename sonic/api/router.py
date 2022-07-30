from fastapi import APIRouter

from sonic.api import add_transaction

api_router = APIRouter()

api_router.include_router(
    add_transaction.router, prefix="/transactions", tags=["transactions"]
)

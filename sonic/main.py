import logging

from fastapi import FastAPI

from sonic.api.router import api_router

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.include_router(api_router)

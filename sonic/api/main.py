from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

from sonic.api import transactions
from sonic.monitoring import logger, setup_logging, setup_telemetry
from sonic.settings import Settings

settings = Settings()
setup_logging()
setup_telemetry(settings.telemetry)

app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(f"{request}: {exc_str}")

    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

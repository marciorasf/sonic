from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

from sonic.api.router import api_router
from sonic.logging import setup_logging
from sonic.settings import Settings
from sonic.telemetry import setup_telemetry

settings = Settings()
setup_logging()
setup_telemetry(settings.telemetry)

app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


app.include_router(api_router)

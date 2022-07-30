import logging

import orjson
import structlog
from fastapi import FastAPI
from opentelemetry import trace  # type: ignore[attr-defined]
from opentelemetry.exporter.jaeger.thrift import (  # type: ignore[attr-defined]
    JaegerExporter,
)
from opentelemetry.sdk.resources import (  # type: ignore[attr-defined]
    SERVICE_NAME,
    Resource,
)
from opentelemetry.sdk.trace import TracerProvider  # type: ignore[attr-defined]
from opentelemetry.sdk.trace.export import (  # type: ignore[attr-defined]
    BatchSpanProcessor,
)
from starlette_exporter import PrometheusMiddleware, handle_metrics

from sonic.api.router import api_router
from sonic.settings import Settings

structlog.configure(
    cache_logger_on_first_use=True,
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.JSONRenderer(serializer=orjson.dumps),
    ],
    logger_factory=structlog.BytesLoggerFactory(),
)

settings = Settings()

resource = Resource(attributes={SERVICE_NAME: settings.jaeger.service})

jaeger_exporter = JaegerExporter(
    agent_host_name=settings.jaeger.host,
    agent_port=settings.jaeger.port,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.include_router(api_router)

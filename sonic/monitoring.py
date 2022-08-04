import logging
from typing import TYPE_CHECKING

import orjson
import structlog
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

if TYPE_CHECKING:
    from sonic.settings import TelemetryConfig


def setup_telemetry(config: "TelemetryConfig") -> None:
    resource = Resource(attributes={SERVICE_NAME: config.service})

    jaeger_exporter = JaegerExporter(
        agent_host_name=config.host,
        agent_port=config.port,
    )

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(jaeger_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def setup_logging() -> None:
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


logger = structlog.stdlib.get_logger()

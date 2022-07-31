from pydantic import BaseModel, BaseSettings


class TelemetryConfig(BaseModel):
    service: str = "sonic"
    host: str = "localhost"
    port: int = 6831


class Settings(BaseSettings):
    telemetry: TelemetryConfig = TelemetryConfig()

    class Config:
        env_prefix = "sonic_"
        env_nested_delimiter = "__"
        allow_mutation = False

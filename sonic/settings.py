from pydantic import BaseModel, BaseSettings


class Jaeger(BaseModel):
    service: str = "sonic"
    host: str = "localhost"
    port: int = 6831


class Settings(BaseSettings):
    jaeger: Jaeger = Jaeger()

    class Config:
        env_prefix = "sonic_"
        env_nested_delimiter = "__"
        allow_mutation = False

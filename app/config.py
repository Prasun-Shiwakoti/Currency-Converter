from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Currency Converter API"
    exchange_rate_api_url: HttpUrl
    exchange_rate_api_key: str
    redis_host_url: str
    redis_host_port: int
    app_host_url: str
    app_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings():
    return Settings()

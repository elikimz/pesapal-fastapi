from functools import lru_cache

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    api_key: str = Field(..., alias="API_KEY")
    email: str = Field(..., alias="EMAIL")
    pesaflux_base_url: HttpUrl = Field(
        "https://api.pesaflux.co.ke/v1",
        alias="PESAFLUX_BASE_URL",
    )
    request_timeout_seconds: int = Field(30, alias="REQUEST_TIMEOUT_SECONDS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

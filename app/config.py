"""Application configuration."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # PesaFlux API credentials (Hardcoded as requested)
    api_key: str = "PSFXmLezf0Zf"
    email: str = "frankkhayumbi10@gmail.com"
    pesaflux_base_url: str = "https://api.pesaflux.co.ke/v1"

    # CORS – comma-separated list of allowed origins
    allowed_origins: str = "*"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()

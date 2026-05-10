"""Application configuration."""
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database - Use SQLite by default (no external DB needed)
    database_url: str = "sqlite:///./pesaflux.db"
    
    # PesaFlux API
    pesaflux_api_key: str = "PSFXmLezf0Zf"
    pesaflux_email: str = "frankkhayumbi10@gmail.com"
    pesaflux_base_url: str = "https://api.pesaflux.co.ke/v1"
    
    # Callback
    callback_url: str = "http://localhost:8000/callback"
    
    # Server
    debug: bool = False  # Set to False for production
    secret_key: str = "pesaflux-secret-key-2024-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow environment variables to override defaults
        extra = "allow"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

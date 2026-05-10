"""Application configuration."""
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/pesaflux_db"
    
    # PesaFlux API
    pesaflux_api_key: str = "PSFXmLezf0Zf"
    pesaflux_email: str = "frankkhayumbi10@gmail.com"
    pesaflux_base_url: str = "https://api.pesaflux.co.ke/v1"
    
    # Callback
    callback_url: str = "http://localhost:8000/callback"
    
    # Server
    debug: bool = True
    secret_key: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

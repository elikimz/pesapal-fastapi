import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PESAFLUX_API_KEY: str = os.getenv("PESAFLUX_API_KEY", "")
    PESAFLUX_EMAIL: str = os.getenv("PESAFLUX_EMAIL", "")
    PESAFLUX_BASE_URL: str = os.getenv(
        "PESAFLUX_BASE_URL", "https://api.pesaflux.co.ke"
    )


settings = Settings()
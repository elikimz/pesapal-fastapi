import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PESAPAL_CONSUMER_KEY = os.getenv("PESAPAL_CONSUMER_KEY", "")
    PESAPAL_CONSUMER_SECRET = os.getenv("PESAPAL_CONSUMER_SECRET", "")
    PESAPAL_BASE_URL = os.getenv("PESAPAL_BASE_URL", "https://cybqa.pesapal.com/pesapalv3/api")

    PESAPAL_IPN_ID = os.getenv("PESAPAL_IPN_ID", "")
    PESAPAL_CALLBACK_URL = os.getenv("PESAPAL_CALLBACK_URL", "")

settings = Settings()
import time
import httpx
from app.core.config import settings

_token_cache = {"token": None, "exp": 0}

async def get_token() -> str:
    now = time.time()
    if _token_cache["token"] and now < _token_cache["exp"]:
        return _token_cache["token"]

    url = f"{settings.PESAPAL_BASE_URL}/Auth/RequestToken"
    payload = {
        "consumer_key": settings.PESAPAL_CONSUMER_KEY,
        "consumer_secret": settings.PESAPAL_CONSUMER_SECRET,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json=payload, headers={"Accept": "application/json"})
        r.raise_for_status()
        data = r.json()

    token = data["token"]
    _token_cache["token"] = token
    _token_cache["exp"] = now + 240  # cache ~4 mins
    return token


async def submit_order(*, merchant_ref: str, amount: float, email: str, phone: str | None = None):
    if not settings.PESAPAL_IPN_ID:
        raise RuntimeError("Missing PESAPAL_IPN_ID. Register IPN first and set it in .env")

    token = await get_token()
    url = f"{settings.PESAPAL_BASE_URL}/Transactions/SubmitOrderRequest"

    payload = {
        "id": merchant_ref,
        "currency": "KES",
        "amount": float(amount),
        "description": "Payment",
        "callback_url": settings.PESAPAL_CALLBACK_URL,
        "notification_id": settings.PESAPAL_IPN_ID,
        "billing_address": {
            "email_address": email,
            "phone_number": phone,
            "country_code": "KE",
        },
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        r.raise_for_status()
        return r.json()
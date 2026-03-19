"""
Pesaflux STK Push service.

Docs: https://api.pesaflux.co.ke/documentation
Endpoint: POST /v1/initiatestk
"""

import uuid
import httpx
from app.core.config import settings


async def initiate_stk_push(phone: str, amount: float, reference: str | None = None) -> dict:
    """
    Send an STK Push request via Pesaflux sandbox.

    Args:
        phone:     Customer phone number (e.g. 254712345678 or 0712345678).
        amount:    Amount in KES.
        reference: Optional unique transaction reference.

    Returns:
        Parsed JSON response from Pesaflux.

    Raises:
        httpx.HTTPStatusError: on non-2xx HTTP response.
        RuntimeError: if PESAFLUX_API_KEY or PESAFLUX_EMAIL are not configured.
    """
    if not settings.PESAFLUX_API_KEY or not settings.PESAFLUX_EMAIL:
        raise RuntimeError(
            "PESAFLUX_API_KEY and PESAFLUX_EMAIL must be set in .env"
        )

    if reference is None:
        reference = str(uuid.uuid4())

    payload = {
        "api_key": settings.PESAFLUX_API_KEY,
        "email": settings.PESAFLUX_EMAIL,
        "amount": str(amount),
        "msisdn": phone,
        "reference": reference,
    }

    url = f"{settings.PESAFLUX_BASE_URL}/v1/initiatestk"

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()


async def check_transaction_status(transaction_request_id: str) -> dict:
    """
    Check the status of a previously initiated STK Push transaction.

    Args:
        transaction_request_id: The transaction_request_id returned by initiate_stk_push.

    Returns:
        Parsed JSON response from Pesaflux.
    """
    if not settings.PESAFLUX_API_KEY or not settings.PESAFLUX_EMAIL:
        raise RuntimeError(
            "PESAFLUX_API_KEY and PESAFLUX_EMAIL must be set in .env"
        )

    payload = {
        "api_key": settings.PESAFLUX_API_KEY,
        "email": settings.PESAFLUX_EMAIL,
        "transaction_request_id": transaction_request_id,
    }

    url = f"{settings.PESAFLUX_BASE_URL}/v1/transactionstatus"

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()

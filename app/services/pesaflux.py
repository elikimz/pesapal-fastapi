from typing import Any

import requests
from fastapi import HTTPException, status

from app.core.config import Settings


def initiate_stk_push(*, amount: str, phone: str, reference: str, settings: Settings) -> dict[str, Any]:
    """Initiate an M-Pesa STK Push request through Pesaflux.

    The Pesaflux response body is returned unchanged so the frontend can display
    the provider message directly. Transport-level and invalid JSON failures are
    converted into clear HTTP errors.
    """

    endpoint = f"{str(settings.pesaflux_base_url).rstrip('/')}/initiatestk"
    payload = {
        "api_key": settings.api_key,
        "email": settings.email,
        "amount": amount,
        "msisdn": phone,
        "reference": reference,
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            timeout=settings.request_timeout_seconds,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "message": "Unable to connect to Pesaflux. Please try again.",
                "error": str(exc),
            },
        ) from exc

    try:
        response_body = response.json()
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "message": "Pesaflux returned a non-JSON response.",
                "status_code": response.status_code,
                "response": response.text,
            },
        ) from exc

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response_body)

    return response_body

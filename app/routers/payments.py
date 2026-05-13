"""Payment endpoints."""
import logging
import uuid
import requests

from fastapi import APIRouter, HTTPException, status

from app.config import get_settings
from app.schemas import STKPushRequest, STKPushResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/payments", tags=["payments"])
settings = get_settings()


def _initiate_stk_push(amount: float, msisdn: str, reference: str) -> dict:
    """Call the Pesaflux STK Push API and return the parsed JSON response."""
    if not settings.api_key or not settings.email:
        logger.error("Pesaflux API credentials (API_KEY or EMAIL) are not configured.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment gateway is not configured.",
        )

    url = f"{settings.pesaflux_base_url}/initiatestk"
    payload = {
        "api_key": settings.api_key,
        "email": settings.email,
        "amount": amount,
        "msisdn": msisdn,
        "reference": reference,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        logger.error("Pesaflux API error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not reach the payment gateway. Please try again.",
        )


@router.post(
    "/stk-push",
    response_model=STKPushResponse,
    summary="Initiate M-Pesa STK Push",
    status_code=status.HTTP_200_OK,
)
async def stk_push(request: STKPushRequest) -> STKPushResponse:
    """
    Initiate an STK Push payment via Pesaflux.
    """
    reference = request.reference or f"PAY-{uuid.uuid4().hex[:8].upper()}"

    logger.info(
        "Initiating STK push | phone=%s | amount=%s | reference=%s",
        request.phone,
        request.amount,
        reference,
    )

    pesaflux_data = _initiate_stk_push(
        amount=request.amount,
        msisdn=request.phone,
        reference=reference,
    )

    return STKPushResponse(
        status="success",
        message="STK Push sent. Please check your phone and enter your M-Pesa PIN.",
        reference=reference,
        data=pesaflux_data,
    )

"""
Payment router — Pesaflux STK Push.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.services.pesaflux_service import initiate_stk_push, check_transaction_status

router = APIRouter(prefix="/payment", tags=["Payment"])


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class PaymentRequest(BaseModel):
    phone: str
    amount: float

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip().replace(" ", "").replace("-", "")
        if v.startswith("+"):
            v = v[1:]
        # Accept 07XXXXXXXX → convert to 2547XXXXXXXX
        if v.startswith("0") and len(v) == 10:
            v = "254" + v[1:]
        if not v.startswith("254") or len(v) != 12:
            raise ValueError(
                "Phone must be a valid Kenyan number (e.g. 0712345678 or 254712345678)"
            )
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class PaymentResponse(BaseModel):
    success: bool
    message: str
    transaction_request_id: str | None = None
    raw: dict | None = None


class StatusRequest(BaseModel):
    transaction_request_id: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/initiate", response_model=PaymentResponse)
async def initiate_payment(body: PaymentRequest):
    """
    Initiate an M-Pesa STK Push via Pesaflux.

    The customer will receive a payment prompt on their phone.
    """
    try:
        result = await initiate_stk_push(phone=body.phone, amount=body.amount)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Pesaflux error: {exc}",
        )

    success_code = str(result.get("success", ""))
    transaction_request_id = result.get("transaction_request_id")

    return PaymentResponse(
        success=success_code == "200",
        message=result.get("massage") or result.get("message") or "Request processed",
        transaction_request_id=transaction_request_id,
        raw=result,
    )


@router.post("/status", response_model=dict)
async def payment_status(body: StatusRequest):
    """
    Check the status of a previously initiated STK Push.
    """
    try:
        result = await check_transaction_status(body.transaction_request_id)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Pesaflux error: {exc}",
        )
    return result

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, field_validator

from app.core.config import Settings, get_settings
from app.services.pesaflux import initiate_stk_push

router = APIRouter(tags=["payments"])


class PaymentRequest(BaseModel):
    amount: str = Field(..., min_length=1, examples=["1"])
    phone: str = Field(
        ...,
        pattern=r"^2547\d{8}$",
        examples=["254712345678"],
        description="Safaricom phone number in 2547XXXXXXXX format.",
    )
    reference: str = Field(..., min_length=1, max_length=100, examples=["Order 1001"])

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive_number(cls, value: str) -> str:
        try:
            amount = float(value)
        except ValueError as exc:
            raise ValueError("Amount must be a valid positive number.") from exc

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        return value


@router.post("/pay")
def pay(payload: PaymentRequest, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    return initiate_stk_push(
        amount=payload.amount,
        phone=payload.phone,
        reference=payload.reference,
        settings=settings,
    )

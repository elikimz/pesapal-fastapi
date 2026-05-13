"""Pydantic request / response schemas."""
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator
import re

class STKPushRequest(BaseModel):
    phone: str = Field(..., description="M-Pesa phone number in international format, e.g. 254712345678")
    amount: float = Field(..., gt=0, description="Payment amount in KES (must be greater than 0)")
    reference: Optional[str] = Field(None, max_length=100)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not re.fullmatch(r"254\d{9}", v):
            raise ValueError("Phone number must be in the format 254XXXXXXXXX")
        return v

class STKPushResponse(BaseModel):
    status: str
    message: str
    reference: str
    data: Optional[Any] = None

class PaymentStatusResponse(BaseModel):
    status: str
    message: str
    reference: str

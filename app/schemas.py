"""Pydantic request/response schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any

class PaymentRequest(BaseModel):
    """Payment initiation request."""
    phone: str = Field(..., description="Customer phone number (e.g., 254712345678)")
    amount: float = Field(..., gt=0, description="Payment amount")

class PaymentResponse(BaseModel):
    """Payment response."""
    status: str
    message: str
    reference: str
    data: Optional[Any] = None

class CallbackRequest(BaseModel):
    """PesaFlux callback request."""
    reference: str
    status: str
    amount: float
    phone: str
    transaction_id: Optional[str] = None

class TransactionSchema(BaseModel):
    """Transaction schema."""
    id: int
    phone: str
    amount: float
    reference: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    """Error response."""
    status: str = "error"
    message: str
    error_code: Optional[str] = None

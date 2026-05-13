"""Payment endpoints."""
import logging
import uuid
import requests
import time
from typing import Dict
from fastapi import APIRouter, HTTPException, status, Request
from app.config import get_settings
from app.schemas import STKPushRequest, STKPushResponse, PaymentStatusResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/payments", tags=["payments"])
settings = get_settings()
payment_store: Dict[str, dict] = {}

def _initiate_stk_push(amount: float, msisdn: str, reference: str) -> dict:
    if not settings.api_key or not settings.email:
        raise HTTPException(status_code=500, detail="Payment gateway not configured.")
    url = f"{settings.pesaflux_base_url}/initiatestk"
    payload = {"api_key": settings.api_key, "email": settings.email, "amount": amount, "msisdn": msisdn, "reference": reference}
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
    response.raise_for_status()
    return response.json()

@router.post("/stk-push", response_model=STKPushResponse)
async def stk_push(request: STKPushRequest):
    reference = request.reference or f"PAY-{uuid.uuid4().hex[:8].upper()}"
    pesaflux_data = _initiate_stk_push(amount=request.amount, msisdn=request.phone, reference=reference)
    payment_store[reference] = {"status": "pending", "timestamp": time.time(), "message": "Waiting for customer PIN entry"}
    return STKPushResponse(status="success", message="STK Push sent.", reference=reference, data=pesaflux_data)

@router.post("/callback")
async def payment_callback(request: Request):
    try:
        data = await request.json()
        reference = data.get("reference")
        status_code = data.get("status")
        if reference and reference in payment_store:
            if str(status_code).lower() in ["success", "completed", "0"]:
                payment_store[reference]["status"] = "completed"
                payment_store[reference]["message"] = "Payment successful"
            else:
                payment_store[reference]["status"] = "failed"
                payment_store[reference]["message"] = f"Payment failed: {data.get('message', 'Unknown error')}"
        return {"status": "ok"}
    except Exception: return {"status": "error"}

@router.get("/status/{reference}", response_model=PaymentStatusResponse)
async def get_payment_status(reference: str):
    if reference not in payment_store: raise HTTPException(status_code=404, detail="Not found")
    payment = payment_store[reference]
    if payment["status"] == "pending" and (time.time() - payment["timestamp"] > 120):
        payment["status"] = "timeout"
        payment["message"] = "Payment session timed out"
    return PaymentStatusResponse(status=payment["status"], message=payment["message"], reference=reference)

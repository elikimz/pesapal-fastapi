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

# In-memory storage for payment statuses
payment_store: Dict[str, dict] = {}

def _initiate_stk_push(amount: float, msisdn: str, reference: str) -> dict:
    if not settings.api_key or not settings.email:
        raise HTTPException(status_code=500, detail="Payment gateway not configured.")
    url = f"{settings.pesaflux_base_url}/initiatestk"
    payload = {
        "api_key": settings.api_key, 
        "email": settings.email, 
        "amount": amount, 
        "msisdn": msisdn, 
        "reference": reference
    }
    logger.info("Calling Pesaflux STK Push: %s", url)
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
    response.raise_for_status()
    return response.json()

@router.post("/stk-push", response_model=STKPushResponse)
async def stk_push(request: STKPushRequest):
    reference = request.reference or f"PAY-{uuid.uuid4().hex[:8].upper()}"
    pesaflux_data = _initiate_stk_push(amount=request.amount, msisdn=request.phone, reference=reference)
    
    # Store with a longer timeout for M-Pesa (3 minutes)
    payment_store[reference] = {
        "status": "pending", 
        "timestamp": time.time(), 
        "message": "Waiting for customer PIN entry"
    }
    
    return STKPushResponse(
        status="success", 
        message="STK Push sent. Please enter your PIN.", 
        reference=reference, 
        data=pesaflux_data
    )

@router.post("/callback")
async def payment_callback(request: Request):
    """
    Webhook endpoint for Pesaflux.
    URL to use in Pesaflux Dashboard: 
    https://pesafluxapi-a5dfaaa8h7ebhrfv.southafricanorth-01.azurewebsites.net/api/payments/callback
    """
    try:
        # Pesaflux might send data as JSON or Form data
        data = await request.json()
        logger.info("Received Pesaflux callback: %s", data)
        
        # Robustly look for reference and status in common Pesaflux keys
        reference = data.get("reference") or data.get("Reference") or data.get("bill_ref_number")
        status_code = data.get("status") or data.get("Status") or data.get("result_code")
        
        if reference and reference in payment_store:
            # Check for various success indicators
            success_indicators = ["success", "completed", "0", 0, "SUCCESS"]
            if str(status_code).lower() in [str(s).lower() for s in success_indicators]:
                payment_store[reference]["status"] = "completed"
                payment_store[reference]["message"] = "Payment successful"
                logger.info("Payment SUCCESS for reference: %s", reference)
            else:
                payment_store[reference]["status"] = "failed"
                payment_store[reference]["message"] = f"Payment failed: {data.get('message', 'User cancelled or insufficient funds')}"
                logger.info("Payment FAILED for reference: %s", reference)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error("Error processing callback: %s", e)
        return {"status": "error"}

@router.get("/status/{reference}", response_model=PaymentStatusResponse)
async def get_payment_status(reference: str):
    if reference not in payment_store:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    payment = payment_store[reference]
    
    # Check for timeout (Extended to 180 seconds to be safe)
    if payment["status"] == "pending" and (time.time() - payment["timestamp"] > 180):
        payment["status"] = "timeout"
        payment["message"] = "Payment session timed out. Please try again."

    return PaymentStatusResponse(
        status=payment["status"], 
        message=payment["message"], 
        reference=reference
    )

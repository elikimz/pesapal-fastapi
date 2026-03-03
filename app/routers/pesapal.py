from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_async_db
from app.services.pesapal_services import get_token, submit_order
from app.services.payment_services import create_payment, update_payment_status

router = APIRouter(prefix="/pesapal", tags=["Pesapal"])

@router.get("/token")
async def token():
    return {"token": await get_token()}

class InitiateIn(BaseModel):
    amount: float
    email: EmailStr
    phone: str | None = None

@router.post("/initiate")
async def initiate(body: InitiateIn, db: AsyncSession = Depends(get_async_db)):
    # 1) create payment row in Neon
    payment = await create_payment(db=db, amount=body.amount, currency="KES")

    # 2) create pesapal order -> get redirect_url
    try:
        resp = await submit_order(
            merchant_ref=payment.merchant_reference,
            amount=body.amount,
            email=str(body.email),
            phone=body.phone,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Pesapal error: {e}")

    # 3) store tracking id
    order_tracking_id = resp.get("order_tracking_id") or resp.get("orderTrackingId")
    redirect_url = resp.get("redirect_url") or resp.get("redirectUrl")

    if order_tracking_id:
        await update_payment_status(
            db=db,
            merchant_reference=payment.merchant_reference,
            status_code=0,
            status_description="PENDING",
            order_tracking_id=order_tracking_id,
        )

    return {
        "merchant_reference": payment.merchant_reference,
        "order_tracking_id": order_tracking_id,
        "redirect_url": redirect_url,
    }
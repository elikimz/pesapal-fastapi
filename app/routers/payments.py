from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database   import get_async_db
from app.services.payment_services import create_payment

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/test")
async def test_create_payment(
    amount: float,
    db: AsyncSession = Depends(get_async_db),
):
    payment = await create_payment(db=db, amount=amount)
    return {
        "merchant_reference": payment.merchant_reference,
        "status": payment.status_description,
    }
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.model import Payment


async def create_payment(
    db: AsyncSession,
    amount: float,
    currency: str = "KES",
) -> Payment:
    merchant_reference = str(uuid.uuid4())

    payment = Payment(
        merchant_reference=merchant_reference,
        amount=amount,
        currency=currency,
        status_code=0,  # pending
        status_description="PENDING",
    )

    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    return payment


async def get_payment_by_reference(
    db: AsyncSession,
    merchant_reference: str,
) -> Payment | None:
    result = await db.execute(
        select(Payment).where(Payment.merchant_reference == merchant_reference)
    )
    return result.scalar_one_or_none()


async def update_payment_status(
    db: AsyncSession,
    merchant_reference: str,
    status_code: int,
    status_description: str,
    order_tracking_id: str | None = None,
):
    payment = await get_payment_by_reference(db, merchant_reference)

    if not payment:
        return None

    payment.status_code = status_code
    payment.status_description = status_description

    if order_tracking_id:
        payment.order_tracking_id = order_tracking_id

    await db.commit()
    await db.refresh(payment)

    return payment
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    merchant_reference: Mapped[str] = mapped_column(String(60), unique=True, index=True, nullable=False)
    order_tracking_id: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)

    currency: Mapped[str] = mapped_column(String(5), default="KES", nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    status_code: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status_description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    confirmation_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    payment_account: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
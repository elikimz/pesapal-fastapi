"""SQLAlchemy database models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    """Transaction model."""
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    reference = Column(String(100), nullable=False, unique=True, index=True)
    status = Column(String(20), default="pending")  # pending, success, failed
    pesaflux_response = Column(Text, nullable=True)  # Store raw API response
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Transaction {self.reference} - {self.status}>"

"""Transaction service."""
import logging
import uuid
from sqlalchemy.orm import Session
from app.models import Transaction
from app.schemas import PaymentRequest, CallbackRequest
from app.services.pesaflux import pesaflux_client

logger = logging.getLogger(__name__)

class TransactionService:
    """Service for transaction operations."""
    
    @staticmethod
    def create_transaction(db: Session, request: PaymentRequest) -> Transaction:
        """Create a new transaction."""
        reference = f"TXN{uuid.uuid4().hex[:12].upper()}"
        
        transaction = Transaction(
            phone=request.phone,
            amount=request.amount,
            reference=reference,
            status="pending"
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"Created transaction: {reference}")
        return transaction
    
    @staticmethod
    def initiate_payment(db: Session, transaction: Transaction) -> dict:
        """Initiate payment with PesaFlux."""
        try:
            response = pesaflux_client.initiate_stk_push(
                phone=transaction.phone,
                amount=transaction.amount,
                reference=transaction.reference
            )
            
            # Store response
            transaction.pesaflux_response = str(response)
            db.commit()
            
            return response
            
        except Exception as e:
            logger.error(f"Payment initiation failed: {str(e)}")
            transaction.status = "failed"
            db.commit()
            raise
    
    @staticmethod
    def get_transaction(db: Session, reference: str) -> Transaction:
        """Get transaction by reference."""
        return db.query(Transaction).filter(
            Transaction.reference == reference
        ).first()
    
    @staticmethod
    def update_transaction_status(
        db: Session,
        reference: str,
        status: str,
        response: dict = None
    ) -> Transaction:
        """Update transaction status from callback."""
        transaction = TransactionService.get_transaction(db, reference)
        
        if not transaction:
            logger.warning(f"Transaction not found: {reference}")
            return None
        
        transaction.status = status
        if response:
            transaction.pesaflux_response = str(response)
        
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"Updated transaction {reference} status to {status}")
        return transaction
    
    @staticmethod
    def list_transactions(db: Session, skip: int = 0, limit: int = 100):
        """List all transactions."""
        return db.query(Transaction).offset(skip).limit(limit).all()

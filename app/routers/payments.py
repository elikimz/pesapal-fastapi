"""Payment endpoints."""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PaymentRequest, PaymentResponse, ErrorResponse, TransactionSchema
from app.services.transactions import TransactionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["payments"])

@router.post("/pay", response_model=PaymentResponse)
async def initiate_payment(
    request: PaymentRequest,
    db: Session = Depends(get_db)
):
    """
    Initiate STK Push payment.
    
    - **phone**: Customer phone number (e.g., 254712345678)
    - **amount**: Payment amount (must be > 0)
    """
    try:
        # Validate phone format
        if not request.phone.startswith("254") or len(request.phone) != 12:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone format. Use 254XXXXXXXXX"
            )
        
        # Create transaction
        transaction = TransactionService.create_transaction(db, request)
        logger.info(f"Created transaction: {transaction.reference}")
        
        # Initiate payment with PesaFlux
        pesaflux_response = TransactionService.initiate_payment(db, transaction)
        
        return PaymentResponse(
            status="success",
            message="STK push sent to your phone",
            reference=transaction.reference,
            data=pesaflux_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Payment initiation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment initiation failed"
        )

@router.get("/transactions", response_model=list[TransactionSchema])
async def list_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all transactions."""
    return TransactionService.list_transactions(db, skip, limit)

@router.get("/transactions/{reference}", response_model=TransactionSchema)
async def get_transaction(
    reference: str,
    db: Session = Depends(get_db)
):
    """Get transaction by reference."""
    transaction = TransactionService.get_transaction(db, reference)
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction

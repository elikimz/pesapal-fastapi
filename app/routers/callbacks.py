"""Webhook callback endpoints."""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CallbackRequest, ErrorResponse
from app.services.transactions import TransactionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["callbacks"])

@router.post("/callback")
async def handle_callback(
    request: CallbackRequest,
    db: Session = Depends(get_db)
):
    """
    Handle PesaFlux payment callback.
    
    PesaFlux will POST to this endpoint with payment status.
    """
    try:
        logger.info(f"Received callback for reference: {request.reference}")
        
        # Update transaction status
        transaction = TransactionService.update_transaction_status(
            db,
            reference=request.reference,
            status=request.status,
            response=request.dict()
        )
        
        if not transaction:
            logger.warning(f"Transaction not found: {request.reference}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        logger.info(f"Updated transaction {request.reference} to {request.status}")
        
        return {
            "status": "success",
            "message": "Callback processed",
            "reference": request.reference
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Callback processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Callback processing failed"
        )

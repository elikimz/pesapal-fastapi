"""PesaFlux API client service."""
import requests
import logging
from typing import Dict, Any, Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class PesaFluxClient:
    """PesaFlux API client."""
    
    def __init__(self):
        self.api_key = settings.pesaflux_api_key
        self.email = settings.pesaflux_email
        self.base_url = settings.pesaflux_base_url
        self.timeout = 30
    
    def initiate_stk_push(
        self,
        phone: str,
        amount: float,
        reference: str
    ) -> Dict[str, Any]:
        """
        Initiate STK Push payment.
        
        Args:
            phone: Customer phone number
            amount: Payment amount
            reference: Unique transaction reference
            
        Returns:
            API response dictionary
            
        Raises:
            requests.RequestException: If API call fails
        """
        endpoint = f"{self.base_url}/initiatestk"
        
        payload = {
            "api_key": self.api_key,
            "email": self.email,
            "amount": str(amount),
            "msisdn": phone,
            "reference": reference
        }
        
        try:
            logger.info(f"Calling PesaFlux API for reference: {reference}")
            response = requests.post(
                endpoint,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"PesaFlux response: {result}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"PesaFlux API error: {str(e)}")
            raise

# Singleton instance
pesaflux_client = PesaFluxClient()

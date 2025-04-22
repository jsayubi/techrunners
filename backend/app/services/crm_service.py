import logging
import uuid
from typing import List, Dict, Optional
import json
import requests
from datetime import datetime

from ..models.models import ClientRequirement, OrderInquiry

logger = logging.getLogger(__name__)

class CRMService:
    def __init__(self, api_url: str = None, api_key: str = None):
        """Initialize CRM service with API credentials."""
        self.api_url = api_url or "https://api.example-crm.com/v1"  # Replace with actual CRM API
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
    
    def create_order(self, order_data: Dict) -> str:
        """Create an order in the CRM system."""
        try:
            # In a real implementation, this would make an API call to a CRM system
            # For demonstration, we'll simulate a successful response
            
            # Simulate API call
            # response = requests.post(
            #    f"{self.api_url}/orders",
            #    headers=self.headers,
            #    json=order_data
            # )
            # response.raise_for_status()
            # order_id = response.json().get("order_id")
            
            # For demonstration, generate a mock order ID
            order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            logger.info(f"Created order {order_id} in CRM system")
            return order_id
            
        except Exception as e:
            logger.error(f"Error creating order in CRM: {str(e)}")
            raise ValueError(f"Failed to create order in CRM: {str(e)}")

# Initialize CRM service
crm_service = CRMService()

def create_order_inquiry(
    conversation_id: str,
    client_id: str,
    requirements: List[ClientRequirement],
    price: float
) -> str:
    """Create an order inquiry in the CRM system."""
    try:
        # Create OrderInquiry object
        order_inquiry = OrderInquiry(
            order_id=f"INQ-{uuid.uuid4().hex[:8].upper()}",
            conversation_id=conversation_id,
            client_id=client_id,
            requirements=requirements,
            price=price
        )
        
        # Format data for CRM system
        order_data = {
            "type": "inquiry",
            "client_id": client_id,
            "conversation_reference": conversation_id,
            "requirements": [
                {
                    "feature_id": req.feature_id,
                    "feature_name": req.feature_name,
                    "quantity": req.quantity or 1,
                    "notes": req.notes
                }
                for req in requirements
            ],
            "price": {
                "amount": price,
                "currency": "USD"
            },
            "metadata": {
                "source": "ai_chatbot",
                "created_at": datetime.now().isoformat()
            }
        }
        
        # Create order in CRM
        order_id = crm_service.create_order(order_data)
        
        # Update order inquiry with real order ID
        order_inquiry.order_id = order_id
        
        # In a real implementation, save the order inquiry to database
        # save_order_inquiry(order_inquiry)
        
        return order_id
        
    except Exception as e:
        logger.error(f"Error creating order inquiry: {str(e)}")
        raise ValueError(f"Failed to create order inquiry: {str(e)}") 
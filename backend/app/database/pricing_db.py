import logging
from typing import List, Dict, Optional, Any
import json
import random

logger = logging.getLogger(__name__)

# Mock historical pricing data for demonstration
# In a real application, this would be stored in a database
HISTORICAL_PRICING = [
    {
        "client_id": "client-001",
        "industry": "healthcare",
        "company_size": "large",
        "region": "north_america",
        "features": ["feat-001", "feat-003", "feat-008", "feat-009"],
        "base_price": 36000.00,
        "final_price": 41400.00,
        "margin_factor": 1.15
    },
    {
        "client_id": "client-002",
        "industry": "finance",
        "company_size": "medium",
        "region": "europe",
        "features": ["feat-001", "feat-002", "feat-003", "feat-005"],
        "base_price": 38000.00,
        "final_price": 43700.00,
        "margin_factor": 1.15
    },
    {
        "client_id": "client-003",
        "industry": "technology",
        "company_size": "small",
        "region": "asia",
        "features": ["feat-001", "feat-003", "feat-006"],
        "base_price": 22000.00,
        "final_price": 24200.00,
        "margin_factor": 1.10
    },
    {
        "client_id": "client-004",
        "industry": "retail",
        "company_size": "large",
        "region": "north_america",
        "features": ["feat-001", "feat-002", "feat-003", "feat-004", "feat-005", "feat-009"],
        "base_price": 50000.00,
        "final_price": 58500.00,
        "margin_factor": 1.17
    },
    {
        "client_id": "client-005",
        "industry": "manufacturing",
        "company_size": "medium",
        "region": "europe",
        "features": ["feat-001", "feat-003", "feat-008", "feat-010"],
        "base_price": 52000.00,
        "final_price": 59800.00,
        "margin_factor": 1.15
    }
]

def get_historical_pricing(
    client_id: Optional[str] = None,
    industry: Optional[str] = None,
    company_size: Optional[str] = None,
    region: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get historical pricing data, optionally filtered by client attributes."""
    try:
        # In a real application, this would query a database
        # For demonstration, we'll filter our mock data
        
        filtered_data = HISTORICAL_PRICING
        
        if client_id:
            filtered_data = [d for d in filtered_data if d.get("client_id") == client_id]
        
        if industry:
            filtered_data = [d for d in filtered_data if d.get("industry") == industry]
        
        if company_size:
            filtered_data = [d for d in filtered_data if d.get("company_size") == company_size]
        
        if region:
            filtered_data = [d for d in filtered_data if d.get("region") == region]
        
        return filtered_data
    
    except Exception as e:
        logger.error(f"Error retrieving historical pricing data: {str(e)}")
        return []

def get_pricing_margin(
    industry: Optional[str] = None,
    company_size: Optional[str] = None,
    region: Optional[str] = None
) -> float:
    """Get an appropriate pricing margin based on historical data."""
    try:
        # Get relevant historical pricing data
        historical_data = get_historical_pricing(
            industry=industry,
            company_size=company_size,
            region=region
        )
        
        if historical_data:
            # Calculate average margin from historical data
            margin_factors = [d.get("margin_factor", 1.15) for d in historical_data]
            avg_margin = sum(margin_factors) / len(margin_factors)
            
            # Add some randomness (±2%)
            margin = avg_margin * random.uniform(0.98, 1.02)
            
            # Ensure margin is within acceptable range (12-18%)
            margin = max(1.12, min(1.18, margin))
            
            return margin
        
        # Default margin if no historical data
        return 1.15
    
    except Exception as e:
        logger.error(f"Error calculating pricing margin: {str(e)}")
        return 1.15 
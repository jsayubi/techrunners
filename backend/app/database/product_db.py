import logging
from typing import List, Dict, Optional
import json

from ..models.models import ProductFeature

logger = logging.getLogger(__name__)

# Mock product features for demonstration
# In a real application, this would be stored in a database
PRODUCT_FEATURES = [
    ProductFeature(
        id="feat-001",
        name="Basic Integration",
        description="Standard API integration with your existing systems",
        base_price=10000.00,
        is_addon=False,
        category="integration"
    ),
    ProductFeature(
        id="feat-002",
        name="Advanced Analytics",
        description="Comprehensive data analysis and visualization tools",
        base_price=15000.00,
        is_addon=True,
        category="analytics"
    ),
    ProductFeature(
        id="feat-003",
        name="Multi-user Access",
        description="Support for multiple user accounts with role-based access control",
        base_price=5000.00,
        is_addon=False,
        category="access"
    ),
    ProductFeature(
        id="feat-004",
        name="Real-time Notifications",
        description="Instant alerts and notifications for critical events",
        base_price=3000.00,
        is_addon=True,
        category="communication"
    ),
    ProductFeature(
        id="feat-005",
        name="Custom Reporting",
        description="Tailored reports based on your business requirements",
        base_price=8000.00,
        is_addon=True,
        category="analytics"
    ),
    ProductFeature(
        id="feat-006",
        name="Mobile Access",
        description="Access your data on the go with mobile applications",
        base_price=7000.00,
        is_addon=True,
        category="access"
    ),
    ProductFeature(
        id="feat-007",
        name="Enterprise Support",
        description="24/7 premium support with dedicated account manager",
        base_price=20000.00,
        is_addon=True,
        category="support"
    ),
    ProductFeature(
        id="feat-008",
        name="Data Migration",
        description="Complete transfer of your existing data to our platform",
        base_price=12000.00,
        is_addon=False,
        category="integration"
    ),
    ProductFeature(
        id="feat-009",
        name="Advanced Security",
        description="Enhanced security features including MFA and encryption",
        base_price=9000.00,
        is_addon=True,
        category="security"
    ),
    ProductFeature(
        id="feat-010",
        name="Customization",
        description="Tailor the platform to your specific business needs",
        base_price=25000.00,
        is_addon=True,
        category="customization"
    ),
]

# In-memory storage for development/demo
# In a real application, this would use a persistent database
_product_features = {f.id: f for f in PRODUCT_FEATURES}

def get_product_features() -> List[ProductFeature]:
    """Get all product features."""
    return list(_product_features.values())

def get_product_feature(feature_id: str) -> Optional[ProductFeature]:
    """Get a product feature by ID."""
    return _product_features.get(feature_id)

def get_features_by_category(category: str) -> List[ProductFeature]:
    """Get all product features in a specific category."""
    return [f for f in _product_features.values() if f.category == category]

def search_features(query: str) -> List[ProductFeature]:
    """Search for product features by name or description."""
    query = query.lower()
    return [
        f for f in _product_features.values()
        if query in f.name.lower() or query in f.description.lower()
    ] 
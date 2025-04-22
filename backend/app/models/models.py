from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class Conversation(BaseModel):
    id: str
    client_id: Optional[str] = None
    messages: List[ChatMessage] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    language: str = "en"
    
class ClientRequirement(BaseModel):
    feature_id: str
    feature_name: str
    required: bool = True
    quantity: Optional[int] = None
    notes: Optional[str] = None

class PricingRequest(BaseModel):
    client_id: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    region: Optional[str] = None
    requirements: List[ClientRequirement]
    
class PricingResponse(BaseModel):
    base_price: float
    discount_percentage: Optional[float] = None
    final_price: float
    currency: str = "USD"
    breakdown: Optional[Dict[str, float]] = None
    
class OrderInquiry(BaseModel):
    order_id: str
    conversation_id: str
    client_id: str
    requirements: List[ClientRequirement]
    price: float
    currency: str = "USD"
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.now)
    
class ConversationState(str, Enum):
    GREETING = "greeting"
    PRODUCT_QA = "product_qa"
    REQUIREMENTS = "requirements"
    PRICING = "pricing"
    CONFIRMATION = "confirmation"
    HANDOFF = "handoff"
    COMPLETED = "completed"

class ConversationContext(BaseModel):
    state: ConversationState = ConversationState.GREETING
    collected_requirements: List[ClientRequirement] = []
    pricing_info: Optional[PricingResponse] = None
    last_question: Optional[str] = None
    language: str = "en"
    
class ProductFeature(BaseModel):
    id: str
    name: str
    description: str
    base_price: float
    is_addon: bool = False
    category: str 
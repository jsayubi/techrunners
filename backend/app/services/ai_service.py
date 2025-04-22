import logging
import json
import uuid
from typing import Dict, List, Optional, Any, Tuple
import boto3
import random
import os
from datetime import datetime

from ..models.models import (
    ChatMessage, 
    Conversation, 
    ConversationState, 
    ConversationContext,
    ClientRequirement,
    PricingRequest,
    PricingResponse,
    MessageRole
)
from ..database.conversation_db import save_conversation, get_conversation
from ..database.product_db import get_product_features
from ..database.pricing_db import get_historical_pricing

logger = logging.getLogger(__name__)

# Check if we're in development mode
DEV_MODE = os.environ.get('DEV_MODE', 'true').lower() == 'true'

# Initialize AWS Bedrock client
if not DEV_MODE:
    # Try to get credentials from environment variables first
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    
    if aws_access_key and aws_secret_key:
        logger.info(f"Using AWS credentials from environment variables for region {aws_region}")
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
    else:
        # Fall back to credentials file or instance profile
        logger.info(f"Using AWS credentials from credentials file or instance profile")
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region
        )
else:
    bedrock_runtime = None
    logger.info("Using mock AI service in development mode")

# System prompts
GREETING_PROMPT = """You are a friendly and helpful B2B sales support chatbot for a tech company. 
Greet the user warmly. Ask how you can help them with our products and services.
If they mention specific needs, acknowledge them and ask relevant follow-up questions."""

PRODUCT_QA_PROMPT = """You are a knowledgeable B2B sales support chatbot for a tech company.
Answer product questions accurately and completely. Highlight key benefits.
If the customer seems ready to discuss requirements, help guide them to that phase."""

REQUIREMENTS_PROMPT = """You are a B2B sales support chatbot focused on gathering client requirements.
Ask clear questions about what features they need. Clarify what's required vs. optional.
Try to understand their business needs in detail."""

PRICING_PROMPT = """You are a B2B sales support chatbot responsible for providing pricing information.
Based on the collected requirements, present a clear pricing summary.
The price should typically be about 15% above our minimum threshold for profitability."""

CONFIRMATION_PROMPT = """You are a B2B sales support chatbot seeking to confirm an order.
Summarize their requirements and the proposed price. Ask if they would like to proceed.
If they accept, prepare to generate an order inquiry. If they decline, offer to connect with a human rep."""

HANDOFF_PROMPT = """You are a B2B sales support chatbot preparing to hand off to a human sales representative.
Thank the client for their interest. Assure them a sales representative will contact them soon.
Ask for any preferred contact method or timing if that information hasn't been collected."""

SYSTEM_PROMPTS = {
    ConversationState.GREETING: GREETING_PROMPT,
    ConversationState.PRODUCT_QA: PRODUCT_QA_PROMPT,
    ConversationState.REQUIREMENTS: REQUIREMENTS_PROMPT,
    ConversationState.PRICING: PRICING_PROMPT,
    ConversationState.CONFIRMATION: CONFIRMATION_PROMPT,
    ConversationState.HANDOFF: HANDOFF_PROMPT,
}

def get_conversation_context(conversation_id: Optional[str] = None) -> Tuple[str, ConversationContext]:
    """Get or create a conversation and its context."""
    if conversation_id:
        conversation = get_conversation(conversation_id)
        if not conversation:
            conversation_id = str(uuid.uuid4())
            conversation = Conversation(id=conversation_id)
            context = ConversationContext()
        else:
            # Extract context from conversation if available
            last_message = None
            if conversation.messages:
                last_message = conversation.messages[-1]
            
            # Simple logic to determine state based on conversation history
            # In a real system, this would be more sophisticated
            context = ConversationContext(
                state=determine_conversation_state(conversation),
                language=conversation.language
            )
    else:
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(id=conversation_id)
        context = ConversationContext()
    
    return conversation_id, context

def determine_conversation_state(conversation: Conversation) -> ConversationState:
    """Determine the current state of the conversation based on its history."""
    # This is a simplified implementation
    # In a real system, this would use more sophisticated analysis
    if not conversation.messages:
        return ConversationState.GREETING
    
    # Count messages to determine rough state
    message_count = len(conversation.messages)
    
    if message_count <= 2:
        return ConversationState.GREETING
    elif message_count <= 6:
        return ConversationState.PRODUCT_QA
    elif message_count <= 10:
        return ConversationState.REQUIREMENTS
    elif message_count <= 12:
        return ConversationState.PRICING
    elif message_count <= 14:
        return ConversationState.CONFIRMATION
    else:
        return ConversationState.HANDOFF

def analyze_requirements(message: str) -> List[ClientRequirement]:
    """Extract requirements from user message."""
    # In a real system, this would use a more sophisticated NLP approach
    # This is a simplified implementation for demonstration
    requirements = []
    
    # Get available product features
    available_features = get_product_features()
    
    # Simple keyword matching for demonstration
    for feature in available_features:
        if feature.name.lower() in message.lower():
            requirements.append(
                ClientRequirement(
                    feature_id=feature.id,
                    feature_name=feature.name,
                    required=True
                )
            )
    
    return requirements

def generate_ai_response(
    messages: List[Dict[str, str]], 
    system_prompt: str
) -> str:
    """Generate AI response using AWS Bedrock with Claude 3.7 Sonnet."""
    try:
        # In development mode, return mock responses
        if DEV_MODE:
            last_message = messages[-1]["content"] if messages else ""
            
            # Simple rule-based mock responses
            if "hello" in last_message.lower() or "hi" in last_message.lower():
                return "Hello! I'm your B2B sales support assistant. How can I help you today?"
            
            if "price" in last_message.lower() or "cost" in last_message.lower():
                return "Our pricing depends on your specific requirements. Could you tell me more about what features you need?"
            
            if "product" in last_message.lower() or "service" in last_message.lower():
                return "We offer a range of B2B solutions including cloud services, data analytics, and enterprise security. Which area are you most interested in?"
            
            # Default response
            return "Thank you for your message. I'd be happy to discuss our products and services with you. Could you tell me more about your business needs?"

        # Format messages for Claude - fixed to use system as a top-level parameter
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Prepare request body for Claude with system as a top-level parameter
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "temperature": 0.7,
            "system": system_prompt,
            "messages": formatted_messages
        })
        
        # Get model ID from environment variable or use default
        model_id = os.environ.get('BEDROCK_MODEL_ID', 'eu.anthropic.claude-3-7-sonnet-20250219-v1:0')
        
        # Invoke Claude model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=body
        )
        
        # Parse response
        response_body = json.loads(response.get('body').read())
        return response_body.get('content')[0].get('text', "I'm sorry, I couldn't generate a response.")
    
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."

def process_query(
    message: str, 
    conversation_id: Optional[str] = None,
    client_id: Optional[str] = None
) -> Dict[str, Any]:
    """Process a user query and generate a response."""
    # Get or create conversation and context
    conversation_id, context = get_conversation_context(conversation_id)
    
    # Get conversation (or create new if not found)
    conversation = get_conversation(conversation_id) or Conversation(
        id=conversation_id, 
        client_id=client_id
    )
    
    # Update conversation with user message
    user_message = ChatMessage(
        role=MessageRole.USER,
        content=message
    )
    conversation.messages.append(user_message)
    
    # Extract requirements if in the right state
    if context.state == ConversationState.REQUIREMENTS:
        new_requirements = analyze_requirements(message)
        context.collected_requirements.extend(new_requirements)
    
    # Prepare messages for AI
    formatted_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in conversation.messages[-5:]  # Use last 5 messages for context
    ]
    
    # Get system prompt based on state
    system_prompt = SYSTEM_PROMPTS.get(context.state, GREETING_PROMPT)
    
    # Generate AI response
    ai_response = generate_ai_response(formatted_messages, system_prompt)
    
    # Update conversation with assistant message
    assistant_message = ChatMessage(
        role=MessageRole.ASSISTANT,
        content=ai_response
    )
    conversation.messages.append(assistant_message)
    
    # Update conversation timestamp
    conversation.updated_at = datetime.now()
    
    # Transition state if needed
    # This is a simplified implementation
    if context.state == ConversationState.REQUIREMENTS and len(context.collected_requirements) >= 3:
        context.state = ConversationState.PRICING
    
    # Save conversation
    save_conversation(conversation)
    
    # Check if we need to generate pricing
    if context.state == ConversationState.PRICING and not context.pricing_info:
        if context.collected_requirements:
            pricing_request = PricingRequest(
                client_id=client_id,
                requirements=context.collected_requirements
            )
            context.pricing_info = generate_pricing(pricing_request)
    
    # Return response data
    return {
        "conversation_id": conversation_id,
        "message": ai_response,
        "state": context.state
    }

def generate_pricing(request: PricingRequest) -> PricingResponse:
    """Generate pricing based on client requirements."""
    total_price = 0.0
    breakdown = {}
    
    # Get product features
    product_features = {f.id: f for f in get_product_features()}
    
    # Calculate base price from requirements
    for req in request.requirements:
        if req.feature_id in product_features:
            feature = product_features[req.feature_id]
            quantity = req.quantity or 1
            item_price = feature.base_price * quantity
            total_price += item_price
            breakdown[feature.name] = item_price
    
    # Get historical pricing data for similar clients
    historical_data = get_historical_pricing(
        client_id=request.client_id,
        industry=request.industry,
        company_size=request.company_size,
        region=request.region
    )
    
    # Adjust price based on historical data (simplified)
    # In a real system, this would use more sophisticated analysis
    base_price = total_price
    
    # Apply margin (~15% above minimum threshold)
    # For demonstration, we're using a random factor between 1.12 and 1.18
    margin_factor = random.uniform(1.12, 1.18)
    final_price = base_price * margin_factor
    
    return PricingResponse(
        base_price=base_price,
        final_price=final_price,
        breakdown=breakdown
    ) 
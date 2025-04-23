import logging
import json
import uuid
from typing import Dict, List, Optional, Any, Tuple
import boto3
import random
import os
from datetime import datetime
import faiss
import numpy as np


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

# Initialize FAISS index and document store
document_store = []
dimension = 1536  # Dimension of embeddings
faiss_index = faiss.IndexFlatL2(dimension)  # Using L2 distance for similarity

def index_documents_to_faiss(documents: List[Tuple[str, str]]):
    global document_store
    global faiss_index
    vectors = []
    new_docs = []
    for doc_id, content in documents:
        vector = embed_text(content)
        vectors.append(vector)
        new_docs.append(content)
    
    if vectors:
        vectors_np = np.array(vectors).astype('float32')
        if faiss_index.ntotal == 0:
            faiss_index.add(vectors_np)
        else:
            # If index already has vectors, we need to rebuild it
            faiss_index.reset()
            faiss_index.add(vectors_np)
        
        document_store.extend(new_docs)
        logger.info(f"Indexed {len(new_docs)} documents. Total in index: {faiss_index.ntotal}")

def get_documents_from_s3(prefix: str = '') -> List[Tuple[str, str]]:
    """
    Download and return documents from S3.
    Returns list of (doc_id, content).
    """
    docs = []
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    for obj in response.get('Contents', []):
        key = obj['Key']
        file_obj = s3.get_object(Bucket=bucket_name, Key=key)
        content = file_obj['Body'].read().decode('utf-8')
        docs.append((key, content))

    return docs


def embed_text(text: str) -> List[float]:
    """Generate an embedding using Titan Embeddings via Bedrock."""
    if DEV_MODE or bedrock_runtime is None:
        # Return mock embedding in dev mode
        random.seed(hash(text))  # Ensures consistency across calls
        return [random.random() for _ in range(1536)]  # Typical embedding length

    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-embed-text-v2",
        body=json.dumps({
            "inputText": text
        }),
        contentType="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["embedding"]


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
    """Determine the current state of the conversation using semantic intent detection."""
    if not conversation.messages:
        return ConversationState.GREETING

    # Find last user message
    user_messages = [m for m in conversation.messages if m.role == MessageRole.USER]
    if not user_messages:
        return ConversationState.GREETING

    latest_message = user_messages[-1].content
    message_embedding = embed_text(latest_message)

    best_match = ConversationState.GREETING
    best_score = -1.0

    for state, examples in INTENT_EXAMPLES.items():
        for example in examples:
            example_embedding = embed_text(example)
            score = cosine_similarity(message_embedding, example_embedding)

            if score > best_score:
                best_score = score
                best_match = state

    return best_match

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
    system_prompt: str,
    kb_context: Optional[List[str]] = None
) -> str:
    """Generate AI response using AWS Bedrock with Claude 3.7 Sonnet."""
    try:
        if DEV_MODE:
            last_message = messages[-1]["content"] if messages else ""

        # Prepend KB context if provided
        if kb_context:
            combined_context = "\n\n".join(kb_context)
            context_block = {
                "role": "system",
                "content": (
                    "Use the following context from the knowledge base to help answer the user's question:\n\n"
                    f"{combined_context}"
                )
            }
            messages.insert(0, context_block)
        # Format the full payload
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "temperature": 0.7,
            "system": system_prompt,
            "messages": messages
        })

        model_id = os.environ.get('BEDROCK_MODEL_ID', 'eu.anthropic.claude-3-7-sonnet-20250219-v1:0')

        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=body
        )

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
    """Process a user query and generate a response using RAG."""
    
    # Get or create conversation and context
    conversation_id, context = get_conversation_context(conversation_id)
    
    # Retrieve the conversation or start a new one
    conversation = get_conversation(conversation_id) or Conversation(
        id=conversation_id,
        client_id=client_id
    )
    
    # Add the user's new message
    user_message = ChatMessage(
        role=MessageRole.USER,
        content=message
    )
    conversation.messages.append(user_message)
    
    # Extract requirements if applicable
    if context.state == ConversationState.REQUIREMENTS:
        new_requirements = analyze_requirements(message)
        context.collected_requirements.extend(new_requirements)
    
    # Format messages (last 5 messages)
    formatted_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in conversation.messages[-5:]
    ]
    
    # Get system prompt based on current state
    system_prompt = SYSTEM_PROMPTS.get(context.state, GREETING_PROMPT)

    # 🔍 RAG: Retrieve relevant documents from the knowledge base
    kb_context = retrieve_documents_faiss(message)  # You need to implement this

    # 🧠 Generate AI response using Claude with context
    ai_response = generate_ai_response(formatted_messages, system_prompt, kb_context)
    
    # Save AI response in the conversation
    assistant_message = ChatMessage(
        role=MessageRole.ASSISTANT,
        content=ai_response
    )
    conversation.messages.append(assistant_message)
    
    # Update timestamp
    conversation.updated_at = datetime.now()
    
    # Transition to PRICING if enough requirements gathered
    if context.state == ConversationState.REQUIREMENTS and len(context.collected_requirements) >= 3:
        context.state = ConversationState.PRICING

    # Save the updated conversation
    save_conversation(conversation)
    
    # Generate pricing if entering PRICING state
    if context.state == ConversationState.PRICING and not context.pricing_info:
        if context.collected_requirements:
            pricing_request = PricingRequest(
                client_id=client_id,
                requirements=context.collected_requirements
            )
            context.pricing_info = generate_pricing(pricing_request)
    
    # Return response
    return {
        "conversation_id": conversation_id,
        "message": ai_response,
        "state": context.state
    }


def retrieve_documents_faiss(query: str, top_k: int = 5) -> List[str]:
    global faiss_index
    if len(document_store) == 0:
        logger.warning("Document store is empty - returning empty list")
        return []
    
    query_vector = np.array([embed_text(query)]).astype('float32')
    D, I = faiss_index.search(query_vector, top_k)
    
    # Safely retrieve documents, checking indices
    results = []
    for idx in I[0]:
        if 0 <= idx < len(document_store):
            results.append(document_store[idx])
        else:
            logger.warning(f"Invalid document index: {idx}")
    
    return results

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


def cosine_similarity(a: List[float], b: List[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

def run_indexing_pipeline():
    documents = get_documents_from_s3()
    index_documents_to_faiss(documents)

if __name__ != "__main__":
    # System prompts
    GREETING_PROMPT = """You are a friendly and helpful B2B sales support chatbot. 
    Greet the user warmly. Ask how you can help them with our products and services.
    If they mention specific needs, acknowledge them and ask relevant follow-up questions."""

    PRODUCT_QA_PROMPT = """You are a knowledgeable B2B sales support chatbot.
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
    INTENT_EXAMPLES = {
        ConversationState.GREETING: [
            "Hello", "Hi there", "Good morning", "I'm looking for assistance"
        ],
        ConversationState.PRODUCT_QA: [
            "What products do you offer?", "Can you tell me about your services?",
            "What features are included?", "What is your solution for data analytics?"
        ],
        ConversationState.REQUIREMENTS: [
            "I need a system that handles X", "Can you support Y?", "My business requires Z"
        ],
        ConversationState.PRICING: [
            "How much does it cost?", "What's the price?", "Can you give me a quote?"
        ],
        ConversationState.CONFIRMATION: [
            "That sounds good", "I'm interested", "Let's proceed with the order"
        ],
        ConversationState.HANDOFF: [
            "Can I speak to a representative?", "I want to talk to a human", "Please connect me with someone"
        ]
    }

    s3 = boto3.client('s3')
    bucket_name = 'techrunners'
    logger = logging.getLogger(__name__)

    try:
        response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        logger.info(f"S3 connection successful. Found {response.get('KeyCount', 0)} objects")
    except Exception as e:
        logger.error(f"S3 access failed: {str(e)}")

    try:
        run_indexing_pipeline()
        logger.info("FAISS index initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing FAISS index: {str(e)}")

    # Check if we're in development mode
    DEV_MODE = os.environ.get('DEV_MODE', 'true').lower() == 'true'

    # Initialize AWS Bedrock client
    if not DEV_MODE:
        # Try to get credentials from environment variables first
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_REGION', 'eu-north-1')
        
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

    

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import json
import logging
from langdetect import detect
from datetime import datetime

from .services.language_service import translate_to_english, translate_to_target, detect_language
from .services.ai_service import process_query, generate_pricing
from .services.crm_service import create_order_inquiry
from .models.models import ChatMessage, ClientRequirement, PricingRequest, PricingResponse

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="B2B Sales Support Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConversationRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    client_id: Optional[str] = None
    
class OrderRequest(BaseModel):
    conversation_id: str
    client_id: str
    requirements: List[ClientRequirement]
    price: float
    
@app.get("/")
async def root():
    return {"message": "B2B Sales Support Chatbot API"}

@app.post("/chat")
async def chat(request: ConversationRequest):
    try:
        # Log incoming message
        logger.info(f"Received message: {request.message[:50]}...")
        
        # 1. Detect language
        source_language = detect_language(request.message)
        logger.info(f"Detected language: {source_language}")
        
        # 2. Translate to English if not already
        if source_language != 'en':
            english_message = translate_to_english(request.message, source_language)
            logger.info(f"Translated to English: {english_message[:50]}...")
        else:
            english_message = request.message
            
        # 3. Process the query with AI
        response_data = process_query(english_message, 
                                      conversation_id=request.conversation_id,
                                      client_id=request.client_id)
        
        # Store the detected language in the response
        response_data["detected_language"] = source_language
        
        # 4. Translate response back if needed
        if source_language != 'en':
            response_data["message"] = translate_to_target(
                response_data["message"], source_language)
        
        return response_data
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pricing")
async def calculate_pricing(request: PricingRequest):
    try:
        # Generate pricing based on requirements
        pricing_response = generate_pricing(request)
        
        return pricing_response
    
    except Exception as e:
        logger.error(f"Error calculating pricing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-order")
async def create_order(request: OrderRequest):
    try:
        # Create an order inquiry in the CRM system
        order_id = create_order_inquiry(
            conversation_id=request.conversation_id,
            client_id=request.client_id,
            requirements=request.requirements,
            price=request.price
        )
        
        return {"order_id": order_id, "status": "created"}
    
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 
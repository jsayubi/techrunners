import logging
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

from ..models.models import Conversation, ChatMessage

logger = logging.getLogger(__name__)

# In-memory storage for development/demo
# In a real application, this would use a persistent database
conversations_db = {}

def save_conversation(conversation: Conversation) -> None:
    """Save a conversation to the database."""
    try:
        # In a real application, this would interact with a database
        # For demonstration, we'll use in-memory storage
        conversations_db[conversation.id] = conversation
        logger.info(f"Saved conversation {conversation.id}")
    except Exception as e:
        logger.error(f"Error saving conversation: {str(e)}")
        raise

def get_conversation(conversation_id: str) -> Optional[Conversation]:
    """Get a conversation from the database by ID."""
    try:
        # In a real application, this would interact with a database
        # For demonstration, we'll use in-memory storage
        conversation = conversations_db.get(conversation_id)
        if conversation:
            logger.info(f"Retrieved conversation {conversation_id}")
        else:
            logger.info(f"Conversation {conversation_id} not found")
        return conversation
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        return None

def list_conversations(client_id: Optional[str] = None, limit: int = 100) -> List[Conversation]:
    """List conversations, optionally filtered by client ID."""
    try:
        # In a real application, this would interact with a database
        # For demonstration, we'll use in-memory storage
        if client_id:
            result = [conv for conv in conversations_db.values() if conv.client_id == client_id]
        else:
            result = list(conversations_db.values())
        
        # Sort by updated_at (most recent first) and limit results
        result.sort(key=lambda x: x.updated_at, reverse=True)
        return result[:limit]
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        return []

def delete_conversation(conversation_id: str) -> bool:
    """Delete a conversation from the database."""
    try:
        # In a real application, this would interact with a database
        # For demonstration, we'll use in-memory storage
        if conversation_id in conversations_db:
            del conversations_db[conversation_id]
            logger.info(f"Deleted conversation {conversation_id}")
            return True
        logger.info(f"Conversation {conversation_id} not found for deletion")
        return False
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        return False

def add_message_to_conversation(conversation_id: str, message: ChatMessage) -> bool:
    """Add a message to an existing conversation."""
    try:
        conversation = get_conversation(conversation_id)
        if not conversation:
            logger.error(f"Conversation {conversation_id} not found")
            return False
        
        conversation.messages.append(message)
        conversation.updated_at = datetime.now()
        save_conversation(conversation)
        logger.info(f"Added message to conversation {conversation_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding message to conversation: {str(e)}")
        return False 
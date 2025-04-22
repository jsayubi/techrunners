import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Configuration for the application."""
    
    # Application settings
    APP_NAME = "B2B Sales Support Chatbot"
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # AWS settings
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")
    
    # AWS Bedrock settings
    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "eu.anthropic.claude-3-7-sonnet-20250219-v1:0")
    
    # Database settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "sales_chatbot")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    
    # CRM settings
    CRM_API_URL = os.getenv("CRM_API_URL", "https://api.example-crm.com/v1")
    CRM_API_KEY = os.getenv("CRM_API_KEY", "")
    
    # RAG settings
    VECTOR_DB_URL = os.getenv("VECTOR_DB_URL", "")
    VECTOR_DB_API_KEY = os.getenv("VECTOR_DB_API_KEY", "")
    VECTOR_DB_NAMESPACE = os.getenv("VECTOR_DB_NAMESPACE", "product_data")
    
    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        """Return all config variables as a dictionary."""
        return {key: value for key, value in cls.__dict__.items() 
                if not key.startswith('__') and not callable(value)}

# Create a config instance
config = Config()

# Database connection string
DATABASE_URL = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}" 
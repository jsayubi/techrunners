import logging
import boto3
import os
from langdetect import detect, LangDetectException
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

# Check if we're in development mode
DEV_MODE = os.environ.get('DEV_MODE', 'true').lower() == 'true'

class TranslationService:
    def __init__(self):
        if not DEV_MODE:
            # Try to get credentials from environment variables first
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            aws_region = os.environ.get('AWS_REGION', 'us-east-1')
            
            if aws_access_key and aws_secret_key:
                logger.info(f"Using AWS credentials from environment variables for region {aws_region}")
                self.translate_client = boto3.client(
                    'translate',
                    region_name=aws_region,
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                )
            else:
                # Fall back to credentials file or instance profile
                logger.info(f"Using AWS credentials from credentials file or instance profile")
                self.translate_client = boto3.client('translate', region_name=aws_region)
        else:
            self.translate_client = None
            logger.info("Using mock translation service in development mode")
        
    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """Translate text from source language to target language using AWS Translate."""
        try:
            if DEV_MODE:
                # Return original text in development mode
                logger.info(f"Mock translation: {source_language} -> {target_language}")
                return f"[{target_language}] {text}"
            
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language
            )
            return response.get('TranslatedText', '')
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            # Fallback to original text if translation fails
            return text

# Initialize translation service
translation_service = TranslationService()

def detect_language(text: str) -> str:
    """Detect the language of the given text."""
    try:
        # Clean the text for better detection - remove URLs, emails, special characters
        cleaned_text = text.strip()
        
        # Skip detection for very short texts (less than 10 characters)
        if len(cleaned_text) < 10:
            logger.warning("Text too short for reliable language detection, defaulting to English")
            return 'en'
            
        # Get detected language
        detected_lang = detect(cleaned_text)
        
        # Log the detected language for monitoring
        logger.info(f"Detected language: {detected_lang} for text starting with: {cleaned_text[:30]}...")
        
        return detected_lang
    except LangDetectException as e:
        logger.error(f"Language detection error: {str(e)}")
        # Default to English if detection fails
        return 'en'

def translate_to_english(text: str, source_language: Optional[str] = None) -> str:
    """Translate text to English."""
    if not source_language:
        source_language = detect_language(text)
    
    if source_language == 'en':
        return text
    
    return translation_service.translate(text, source_language, 'en')

def translate_to_target(text: str, target_language: str) -> str:
    """Translate text from English to target language."""
    if target_language == 'en':
        return text
    
    return translation_service.translate(text, 'en', target_language) 
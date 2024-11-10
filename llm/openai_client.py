from typing import Any, Dict
from openai import OpenAI
import json
import logging
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import LLMClient

logger = logging.getLogger(__name__)

class OpenAIClient(LLMClient):
    """OpenAI API client implementation."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini", 
                 system_message: str = None):
        """
        Initialize OpenAI client with API key from env or parameter.
        
        Args:
            api_key: Optional API key. If not provided, will look for OPENAI_API_KEY in environment
            model: OpenAI model to use
            system_message: Custom system message. If not provided, uses game analysis default
        """
        self.load_environment()
        
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please provide it as a parameter "
                "or set OPENAI_API_KEY environment variable."
            )
            
        # Updated client initialization
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.system_message = system_message or (
            "You are a game mechanics analysis system. "
            "Focus on identifying specific gameplay mechanics and their characteristics. "
            "Respond with properly formatted JSON only."
        )
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def call_api(self, prompt: str) -> Dict[str, Any]:
        try:
            # Updated API call syntax
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
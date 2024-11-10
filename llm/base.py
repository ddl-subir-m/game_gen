from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

class LLMClient(ABC):
    """Abstract base class for LLM providers."""
    
    @classmethod
    def load_environment(cls) -> None:
        """Load environment variables from .env file."""
        env_path = Path('.') / '.env'
        if not env_path.exists():
            logger.warning("No .env file found. Expecting environment variables to be set directly.")
        else:
            load_dotenv(env_path)
    
    @abstractmethod
    def call_api(self, prompt: str) -> Dict[str, Any]:
        """Make an API call to the LLM service."""
        pass

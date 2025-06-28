"""
Mistral AI API adapter for LLMInventory.
"""

import json
import requests
from typing import Dict, Any
from .base_adapter import BaseAdapter

class MistralAdapter(BaseAdapter):
    """Adapter for Mistral AI API."""

    def __init__(self, api_key: str):
        """
        Initialize the Mistral adapter.
        
        Args:
            api_key: Mistral API key for authentication.
        """
        super().__init__(api_key)
        self.base_url = "https://api.mistral.ai/v1"

    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a request to Mistral AI API.
        
        Args:
            model_config: Configuration for the model.
            payload: Request payload.
            
        Returns:
            Response from Mistral API.
        """
        url = f"{self.base_url}/chat/completions"
        
        # Mistral uses OpenAI-compatible format
        mistral_payload = {
            "model": model_config['model'],
            **payload
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(mistral_payload),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Mistral API request failed: {str(e)}") 
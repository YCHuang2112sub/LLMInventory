"""
xAI Grok API adapter for LLMInventory.
"""

import json
import requests
from typing import Dict, Any
from .base_adapter import BaseAdapter

class XaiAdapter(BaseAdapter):
    """Adapter for xAI Grok API."""

    def __init__(self, api_key: str):
        """
        Initialize the xAI adapter.
        
        Args:
            api_key: xAI API key for authentication.
        """
        super().__init__(api_key)
        self.base_url = "https://api.x.ai/v1"

    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a request to xAI Grok API.
        
        Args:
            model_config: Configuration for the model.
            payload: Request payload.
            
        Returns:
            Response from xAI API.
        """
        url = f"{self.base_url}/chat/completions"
        
        # xAI uses OpenAI-compatible format
        xai_payload = {
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
                data=json.dumps(xai_payload),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"xAI API request failed: {str(e)}") 
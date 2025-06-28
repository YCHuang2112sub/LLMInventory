"""
Google Gemini API adapter for LLMInventory.
"""

import json
import requests
from typing import Dict, Any
from .base_adapter import BaseAdapter

class GoogleAdapter(BaseAdapter):
    """Adapter for Google Gemini API."""

    def __init__(self, api_key: str):
        """
        Initialize the Google adapter.
        
        Args:
            api_key: Google API key for authentication.
        """
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a request to Google Gemini API.
        
        Args:
            model_config: Configuration for the model.
            payload: Request payload.
            
        Returns:
            Response from Google API.
        """
        model_id = model_config['model']
        url = f"{self.base_url}/{model_id}:generateContent"
        
        # Convert messages format to Google's format
        google_payload = self._convert_payload(payload)
        
        headers = {
            "Content-Type": "application/json",
        }
        
        params = {
            "key": self.api_key
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                params=params,
                data=json.dumps(google_payload),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Google API request failed: {str(e)}")

    def _convert_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert standard payload format to Google's expected format.
        
        Args:
            payload: Standard payload with messages.
            
        Returns:
            Google-formatted payload.
        """
        google_payload = {}
        
        # Convert messages to Google's contents format
        if 'messages' in payload:
            contents = []
            for message in payload['messages']:
                role = message.get('role', 'user')
                content = message.get('content', '')
                
                # Map roles
                if role == 'assistant':
                    role = 'model'
                elif role == 'system':
                    # Google doesn't have system role, prepend to first user message
                    if contents and contents[-1]['role'] == 'user':
                        contents[-1]['parts'][0]['text'] = f"{content}\n\n{contents[-1]['parts'][0]['text']}"
                        continue
                    else:
                        role = 'user'
                        content = f"System: {content}"
                
                contents.append({
                    "role": role,
                    "parts": [{"text": content}]
                })
            
            google_payload['contents'] = contents
        
        # Add generation config parameters
        generation_config = {}
        param_mapping = {
            'temperature': 'temperature',
            'max_tokens': 'maxOutputTokens',
            'top_p': 'topP',
            'top_k': 'topK'
        }
        
        for param, google_param in param_mapping.items():
            if param in payload:
                generation_config[google_param] = payload[param]
        
        if generation_config:
            google_payload['generationConfig'] = generation_config
        
        return google_payload 
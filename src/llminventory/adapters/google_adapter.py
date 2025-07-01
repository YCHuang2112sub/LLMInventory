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

    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send a request to Google Gemini API.
        
        Args:
            model_config: Configuration for the model.
            payload: Request payload.
            parameters: Optional parameters for the request.
            
        Returns:
            Response from Google API.
        """
        model_id = model_config['model']
        
        # Check if this is an embedding model
        capabilities = model_config.get('capabilities', [])
        is_embedding_model = 'embeddings' in capabilities
        
        if is_embedding_model:
            return self._invoke_embedding(model_id, payload, parameters or {})
        else:
            return self._invoke_generation(model_id, payload, parameters or {})

    def _invoke_generation(self, model_id: str, payload: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a request to Google Gemini text generation API.
        
        Args:
            model_id: The model identifier.
            payload: Request payload.
            parameters: Optional parameters for the request.
            
        Returns:
            Response from Google API.
        """
        url = f"{self.base_url}/{model_id}:generateContent"
        
        # Convert messages format to Google's format
        google_payload = self._convert_payload(payload, parameters)
        
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

    def _invoke_embedding(self, model_id: str, payload: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a request to Google embedding API.
        
        Args:
            model_id: The model identifier.
            payload: Request payload with 'input' field.
            parameters: Optional parameters for the request.
            
        Returns:
            Response from Google API.
        """
        url = f"{self.base_url}/{model_id}:embedContent"
        
        # Convert payload to Google's embedding format
        google_payload = self._convert_embedding_payload(payload, parameters)
        
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

    def _convert_payload(self, payload: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Convert standard payload format to Google's expected format.
        
        Args:
            payload: Standard payload with messages.
            parameters: Optional parameters for generation.
            
        Returns:
            Google-formatted payload.
        """
        google_payload = {}
        parameters = parameters or {}
        
        # Handle Google's native format
        if 'contents' in payload:
            google_payload['contents'] = payload['contents']
        # Convert messages to Google's contents format
        elif 'messages' in payload:
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
        
        # Add generation config parameters from both payload and parameters
        generation_config = {}
        param_mapping = {
            'temperature': 'temperature',
            'max_tokens': 'maxOutputTokens',
            'maxOutputTokens': 'maxOutputTokens',
            'top_p': 'topP',
            'topP': 'topP',
            'top_k': 'topK',
            'topK': 'topK'
        }
        
        # Check both payload and parameters for config values
        all_params = {**payload, **parameters}
        for param, google_param in param_mapping.items():
            if param in all_params:
                generation_config[google_param] = all_params[param]
        
        if generation_config:
            google_payload['generationConfig'] = generation_config
        
        return google_payload 

    def _convert_embedding_payload(self, payload: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Convert standard payload format to Google's embedding format.
        
        Args:
            payload: Standard payload with 'input' field.
            parameters: Optional parameters for embedding.
            
        Returns:
            Google-formatted embedding payload.
        """
        google_payload = {}
        parameters = parameters or {}
        
        # Handle input text
        if 'input' in payload:
            input_text = payload['input']
            if isinstance(input_text, str):
                google_payload['content'] = {
                    "parts": [{"text": input_text}]
                }
            elif isinstance(input_text, list):
                # Handle multiple inputs
                google_payload['content'] = {
                    "parts": [{"text": text} for text in input_text]
                }
        
        # Handle optional parameters
        if 'dimensions' in parameters:
            google_payload['outputDimensionality'] = parameters['dimensions']
        
        # Handle task type if specified
        if 'task_type' in parameters:
            google_payload['taskType'] = parameters['task_type']
        
        return google_payload
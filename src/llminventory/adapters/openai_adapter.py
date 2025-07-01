"""Adapter for interacting with OpenAI's API."""

import requests
from typing import Dict, Any
from .base_adapter import BaseAdapter

class OpenAIAdapter(BaseAdapter):
    """Adapter for making requests to the OpenAI API."""

    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Sends a request to the OpenAI API (chat completions or image generation).

        Args:
            model_config: The configuration for the OpenAI model.
            payload: The request payload, format depends on model type.
            parameters: Optional parameters for the request.

        Returns:
            The JSON response from the API.

        Raises:
            ConnectionError: If the request to the API fails.
        """
        endpoint = model_config['endpoint']
        model_name = model_config['model']
        capabilities = model_config.get('capabilities', [])
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Handle different model types
        if 'image_generation' in capabilities:
            # DALL-E models - image generation
            request_body = self._prepare_image_request(model_name, payload, parameters)
        else:
            # Chat completion models
            request_body = self._prepare_chat_request(model_name, payload, parameters)

        try:
            response = requests.post(endpoint, headers=headers, json=request_body, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to OpenAI API at {endpoint}: {e}") from e
    
    def _prepare_chat_request(self, model: str, payload: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Prepare request body for chat completion models."""
        request_body = {"model": model, **payload}
        if parameters:
            request_body.update(parameters)
        return request_body
    
    def _prepare_image_request(self, model: str, payload: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Prepare request body for image generation models (DALL-E)."""
        request_body = {"model": model}
        
        # Handle different payload formats
        if 'prompt' in payload:
            # Direct prompt format
            request_body['prompt'] = payload['prompt']
        elif 'messages' in payload:
            # Convert messages to prompt
            messages = payload['messages']
            if messages and len(messages) > 0:
                # Extract prompt from last user message
                last_message = messages[-1]
                if last_message.get('role') == 'user':
                    request_body['prompt'] = last_message.get('content', '')
                else:
                    # Fallback: concatenate all user messages
                    user_messages = [msg.get('content', '') for msg in messages if msg.get('role') == 'user']
                    request_body['prompt'] = ' '.join(user_messages)
            else:
                raise ValueError("No valid prompt found in messages")
        else:
            raise ValueError("DALL-E requires either 'prompt' field or 'messages' with user content")
        
        # Add image-specific parameters
        if parameters:
            # Map common parameters to DALL-E format
            param_mapping = {
                'size': 'size',
                'quality': 'quality', 
                'style': 'style',
                'n': 'n'
            }
            
            for param_key, dalle_key in param_mapping.items():
                if param_key in parameters:
                    request_body[dalle_key] = parameters[param_key]
        
        # Set defaults if not specified
        if 'size' not in request_body:
            request_body['size'] = "1024x1024"
        if 'n' not in request_body:
            request_body['n'] = 1
            
        return request_body
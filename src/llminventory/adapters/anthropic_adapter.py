"""Adapter for interacting with Anthropic's API."""

import requests
from typing import Dict, Any, List
from .base_adapter import BaseAdapter

class AnthropicAdapter(BaseAdapter):
    """Adapter for making requests to the Anthropic API."""

    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Sends a request to the Anthropic API messages endpoint.

        Args:
            model_config: The configuration for the Anthropic model.
            payload: The request payload, containing 'messages'.
            parameters: Optional parameters for the request (temperature, max_tokens, etc.).

        Returns:
            The JSON response from the API.

        Raises:
            ConnectionError: If the request to the API fails.
        """
        endpoint = model_config['endpoint']
        headers = {
            "X-API-Key": self.api_key,
            "anthropic-version": "2023-06-01",  # Use a supported version
            "Content-Type": "application/json"
        }

        # Adapt the payload to Anthropic's expected format
        # Anthropic expects "system" and "messages" (list of user/assistant turns)
        anthropic_messages: List[Dict[str, Any]] = []
        for message in payload.get("messages", []):
            role = message.get("role")
            if role == "user":
                anthropic_messages.append({"role": "user", "content": message.get("content")})
            elif role == "assistant":
                anthropic_messages.append({"role": "assistant", "content": message.get("content")})
            # In a more complete implementation, we might need to handle system messages
            # or adapt other roles as needed.

        request_body = {
            "model": model_config['model'],
            "messages": anthropic_messages,
            **{k: v for k, v in payload.items() if k != "messages"}  # Add other params except original messages
        }
        
        # Add parameters if provided
        if parameters:
            request_body.update(parameters)

        try:
            response = requests.post(endpoint, headers=headers, json=request_body, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Anthropic API at {endpoint}: {e}") from e
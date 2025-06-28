"""Adapter for interacting with OpenAI's API."""

import requests
from typing import Dict, Any
from .base_adapter import BaseAdapter

class OpenAIAdapter(BaseAdapter):
    """Adapter for making requests to the OpenAI API."""

    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a request to the OpenAI API chat completions endpoint.

        Args:
            model_config: The configuration for the OpenAI model.
            payload: The request payload, containing 'messages' and other parameters.

        Returns:
            The JSON response from the API.

        Raises:
            ConnectionError: If the request to the API fails.
        """
        endpoint = model_config['endpoint']
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # The payload already contains merged and validated parameters.
        # We just need to add the model name to the request body.
        request_body = {"model": model_config['model'], **payload}

        try:
            response = requests.post(endpoint, headers=headers, json=request_body, timeout=60)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to OpenAI API at {endpoint}: {e}") from e
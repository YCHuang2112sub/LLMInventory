"""Defines the abstract base class for all provider adapters."""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    """Abstract base class for all provider adapters."""

    def __init__(self, api_key: str):
        """Initializes the adapter with the necessary API key."""
        self.api_key = api_key

    @abstractmethod
    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Sends a request to the provider's API and returns the response.

        Args:
            model_config: The configuration for the specific model being invoked.
            payload: The user-provided data, including required fields.
            parameters: Optional parameters for the request (temperature, max_tokens, etc.).

        Returns:
            The JSON response from the provider's API as a dictionary.
        """
        pass
"""Defines the abstract base class for all provider adapters."""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    """Abstract base class for all provider adapters."""

    def __init__(self, api_key: str):
        """Initializes the adapter with the necessary API key."""
        self.api_key = api_key

    @abstractmethod
    def invoke(self, model_config: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a request to the provider's API and returns the response.

        Args:
            model_config: The configuration for the specific model being invoked.
            payload: The user-provided data, including required fields and parameters.

        Returns:
            The JSON response from the provider's API as a dictionary.
        """
        pass
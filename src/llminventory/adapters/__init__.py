"""
This package contains the provider-specific adapters for the LLMInventory.
It exposes a factory function to retrieve the correct adapter class.
"""

from .base_adapter import BaseAdapter
from .anthropic_adapter import AnthropicAdapter
from .google_adapter import GoogleAdapter
from .openai_adapter import OpenAIAdapter
from .xai_adapter import XaiAdapter
from .mistral_adapter import MistralAdapter

def get_adapter(provider_name: str) -> type[BaseAdapter]:
    """
    Returns the adapter class for a given provider.

    Args:
        provider_name: The name of the provider (e.g., 'openai').

    Returns:
        The corresponding adapter class.

    Raises:
        ValueError: If no adapter is found for the provider.
    """
    adapters = {
        "openai": OpenAIAdapter,
        "anthropic": AnthropicAdapter,
        "google": GoogleAdapter,
        "xai": XaiAdapter,
        "mistral": MistralAdapter,
    }
    adapter_class = adapters.get(provider_name.lower())
    if not adapter_class:
        raise ValueError(f"No adapter found for provider: {provider_name}")
    return adapter_class
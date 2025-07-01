"""
Provides a high-level programmatic interface for the LLMInventory.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional

from .secret_manager import SecretManager
from .model_config_manager import ModelConfigManager
from .adapters import get_adapter

class LLMInventory:
    """A class providing a direct, function-call interface to the LLM inventory."""

    def __init__(
        self,
        configs_dir: Path,
        secrets_file: Optional[Path] = None
    ):
        """
        Initializes the LLMInventory.

        Args:
            configs_dir: The path to the directory containing model YAML configs.
            secrets_file: The path to the YAML file containing API secrets.
        """
        self.model_config_manager = ModelConfigManager(configs_dir)
        self.secret_manager = SecretManager()
        if secrets_file and secrets_file.is_file():
            self.secret_manager.load_secrets(secrets_file)
        elif secrets_file:
            print(f"Warning: Secrets file not found at {secrets_file}. API calls will likely fail.")

    def get_supported_models(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all supported models and their configurations.
        """
        all_model_names = self.model_config_manager.get_all_model_names()
        model_details = []
        for name in sorted(all_model_names):
            provider, model_name = name.split('/', 1)
            config = self.model_config_manager.get_model_config(provider, model_name)
            if config:
                model_details.append(config)
        return model_details

    def invoke(
        self,
        provider: str,
        model: str,
        payload: Dict[str, Any],
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Sends a request to a specified model and returns the provider's response.

        Args:
            provider: The name of the provider (e.g., 'openai').
            model: The specific model name (e.g., 'gpt-4-turbo').
            payload: The main request payload, containing required fields like 'messages'.
            parameters: Optional model parameters to override defaults.

        Returns:
            The JSON response from the provider's API as a dictionary.

        Raises:
            KeyError: If the model is not found or the API key is missing.
            ValueError: If required fields are missing or parameters are invalid.
            ConnectionError: If the request to the provider API fails.
        """
        model_config = self.model_config_manager.get_model_config(provider, model)
        if not model_config:
            raise KeyError(f"Model not found: {provider}/{model}")

        # Check required fields, but allow adapters to handle conversions
        required_fields = model_config.get('required_fields', [])
        capabilities = model_config.get('capabilities', [])
        
        # Special handling for image generation models
        if 'image_generation' in capabilities and provider == 'openai':
            # For DALL-E, accept either 'prompt' or 'messages' format
            if 'prompt' not in payload and 'messages' not in payload:
                raise ValueError("DALL-E models require either 'prompt' field or 'messages' field")
        else:
            # Standard required field validation
            for field in required_fields:
                if field not in payload:
                    raise ValueError(f"Missing required field in payload: '{field}'")

        final_params = self.model_config_manager.merge_and_validate_params(
            provider, model, parameters
        )

        api_key = self.secret_manager.get_secret(provider)
        if not api_key:
            raise KeyError(f"API key for provider '{provider}' not found in secrets.")

        adapter_class = get_adapter(provider)
        adapter = adapter_class(api_key=api_key)

        response = adapter.invoke(model_config, payload, final_params)
        return response
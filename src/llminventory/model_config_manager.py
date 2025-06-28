"""Manages loading, validating, and providing access to LLM model configurations."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List

class ModelConfigManager:
    """
    Manages loading, validating, and providing access to LLM model configurations.
    """

    def __init__(self, configs_dir: Path):
        """
        Initializes the ModelConfigManager by loading all model configurations.

        Args:
            configs_dir: The path to the directory containing model config files.
        """
        self.configs_dir = configs_dir
        self._model_configs: Dict[str, Dict[str, Any]] = {}
        self._load_all_configs()

    def _load_all_configs(self) -> None:
        """
        Loads model configurations from supported_models.yaml file in the project root.
        Falls back to individual YAML files in configs directory if the main file doesn't exist.
        """
        # First try to load from the main supported_models.yaml file
        project_root = self.configs_dir.parent
        supported_models_file = project_root / "supported_models.yaml"
        
        if supported_models_file.exists():
            try:
                with open(supported_models_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                    # Handle both list format (current) and dict format (future)
                    models_data = []
                    if isinstance(data, list):
                        models_data = data
                    elif isinstance(data, dict) and 'models' in data:
                        if isinstance(data['models'], dict):
                            # New format: dict of models
                            for model_key, model_config in data['models'].items():
                                models_data.append(model_config)
                        elif isinstance(data['models'], list):
                            # Alternative format: list under 'models' key
                            models_data = data['models']
                    
                    # Process models
                    for model_config in models_data:
                        provider = model_config.get('provider')
                        model_id = model_config.get('model') or model_config.get('model_id')
                        
                        if provider and model_id:
                            # Use existing config if it has the right structure, or convert if needed
                            if 'endpoint' in model_config and 'parameters' in model_config:
                                # Already in the right format (from individual config files)
                                config = model_config
                            else:
                                # Convert from comprehensive format
                                config = {
                                    'provider': provider,
                                    'model': model_id,
                                    'endpoint': self._get_endpoint_for_provider(provider),
                                    'description': model_config.get('description', ''),
                                    'parameters': self._convert_default_params_to_parameter_schema(
                                        model_config.get('default_params', {})
                                    ),
                                    'required_fields': self._get_required_fields_for_provider(provider),
                                    'capabilities': model_config.get('capabilities', []),
                                    'context_window': model_config.get('context_window'),
                                    'max_output': model_config.get('max_output'),
                                    'pricing': model_config.get('pricing', {})
                                }
                            
                            key = f"{provider}/{model_id}"
                            self._model_configs[key] = config
                    
                    print(f"Loaded {len(self._model_configs)} models from {supported_models_file}")
                    return
                        
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse supported_models.yaml: {e}")
            except Exception as e:
                print(f"Warning: Error loading supported_models.yaml: {e}")
        
        # Fallback: Load individual config files from configs directory
        print("Falling back to loading individual config files...")
        self._load_individual_configs()

    def _load_individual_configs(self) -> None:
        """
        Loads individual YAML configuration files from the configs directory.
        Each config is stored with a key of "provider/model_name".
        """
        if not self.configs_dir.is_dir():
            raise NotADirectoryError(f"Configs directory not found: {self.configs_dir}")

        for config_file in self.configs_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    # Basic validation for required top-level keys
                    required_top_level_keys = ['provider', 'model', 'endpoint', 'description', 'parameters', 'required_fields']
                    if not all(k in config for k in required_top_level_keys):
                        missing_keys = [k for k in required_top_level_keys if k not in config]
                        raise ValueError(f"Missing required fields {missing_keys} in config: {config_file.name}")

                    provider = config['provider']
                    model_name = config['model']
                    key = f"{provider}/{model_name}"
                    self._model_configs[key] = config
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse YAML file {config_file.name}: {e}")
            except ValueError as e:
                print(f"Warning: Invalid config file {config_file.name}: {e}")
            except Exception as e:
                print(f"Warning: An unexpected error occurred loading {config_file.name}: {e}")

    def _get_endpoint_for_provider(self, provider: str) -> str:
        """Get the API endpoint URL for a given provider."""
        endpoints = {
            'openai': 'https://api.openai.com/v1/chat/completions',
            'anthropic': 'https://api.anthropic.com/v1/messages',
            'google': 'https://generativelanguage.googleapis.com/v1beta/models',
            'xai': 'https://api.x.ai/v1/chat/completions',
            'mistral': 'https://api.mistral.ai/v1/chat/completions'
        }
        return endpoints.get(provider, f'https://api.{provider}.com/v1/chat/completions')

    def _get_required_fields_for_provider(self, provider: str) -> List[str]:
        """Get the required fields for a given provider's API."""
        required_fields = {
            'openai': ['messages'],
            'anthropic': ['messages'],
            'google': ['contents'],
            'xai': ['messages'],
            'mistral': ['messages']
        }
        return required_fields.get(provider, ['messages'])

    def _convert_default_params_to_parameter_schema(self, default_params: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Convert default parameters to the expected parameter schema format."""
        schema = {}
        for param_name, param_value in default_params.items():
            param_type = 'string'
            if isinstance(param_value, bool):
                param_type = 'boolean'
            elif isinstance(param_value, int):
                param_type = 'integer'
            elif isinstance(param_value, float):
                param_type = 'float'
            
            schema[param_name] = {
                'type': param_type,
                'default': param_value
            }
        return schema

    def get_model_config(self, provider: str, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the configuration for a specific model.

        Args:
            provider: The name of the model provider (e.g., 'openai').
            model_name: The specific name of the model (e.g., 'gpt-4-turbo').

        Returns:
            A dictionary containing the model's configuration, or None if not found.
        """
        key = f"{provider}/{model_name}"
        return self._model_configs.get(key)

    def get_all_model_names(self) -> List[str]:
        """
        Returns a list of all loaded model names in 'provider/model' format.
        """
        return list(self._model_configs.keys())

    def merge_and_validate_params(
        self,
        provider: str,
        model_name: str,
        user_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Merges user-provided parameters with model defaults and validates their types.
        Unsupported parameters from user_params are ignored.

        Args:
            provider: The name of the model provider.
            model_name: The specific name of the model.
            user_params: A dictionary of parameters provided by the user.

        Returns:
            A dictionary of validated and merged parameters.

        Raises:
            ValueError: If a user-provided parameter has an invalid type.
            KeyError: If the specified model is not found.
        """
        model_config = self.get_model_config(provider, model_name)
        if not model_config:
            raise KeyError(f"Model '{provider}/{model_name}' not found in configurations.")

        # Initialize merged_params with defaults from the model config
        merged_params: Dict[str, Any] = {}
        if 'parameters' in model_config and model_config['parameters'] is not None:
            for param_name, param_info in model_config['parameters'].items():
                if 'default' in param_info:
                    merged_params[param_name] = param_info['default']

        if user_params:
            for param_name, user_value in user_params.items():
                if param_name in model_config.get('parameters', {}):
                    param_info = model_config['parameters'][param_name]
                    expected_type_str = param_info.get('type')

                    # Type validation
                    type_map = {
                        "float": (float, int), # Allow int to be cast to float
                        "integer": int,
                        "string": str,
                        "boolean": bool
                    }
                    expected_type = type_map.get(expected_type_str)

                    if expected_type and not isinstance(user_value, expected_type):
                        raise ValueError(
                            f"Parameter '{param_name}' for '{provider}/{model_name}' "
                            f"expected type '{expected_type_str}', but got '{type(user_value).__name__}'."
                        )
                    # Handle int -> float conversion explicitly for clarity and robustness
                    if expected_type_str == "float" and isinstance(user_value, int): # If expected is float but user gave int
                        merged_params[param_name] = float(user_value) # Convert int to float
                    elif expected_type_str == "integer" and isinstance(user_value, float) and user_value.is_integer(): # If expected is int but user gave float that is an integer
                        merged_params[param_name] = int(user_value) # Convert float to int
                    else: # Otherwise, use the value as is (after type check)
                        merged_params[param_name] = user_value
                # If param_name is not in model_config.parameters, it's ignored (stripped)

        return merged_params
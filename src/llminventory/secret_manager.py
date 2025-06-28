"""Manages loading and retrieving API secrets from a YAML file."""

import yaml
from pathlib import Path
from typing import Dict, Optional, Any

class SecretManager:
    """Loads and provides access to API keys from a specified secrets file."""

    def __init__(self, secrets_file: Optional[Path] = None):
        """
        Initializes the SecretManager.

        Args:
            secrets_file: The path to the YAML file containing API secrets.
        """
        self._secrets: Dict[str, Any] = {}
        if secrets_file:
            self.load_secrets(secrets_file)

    def load_secrets(self, secrets_file: Path) -> None:
        """
        Loads secrets from the given YAML file.

        Args:
            secrets_file: The path to the YAML secrets file.

        Raises:
            FileNotFoundError: If the secrets file does not exist.
            yaml.YAMLError: If the file is not valid YAML.
        """
        if not secrets_file.is_file():
            raise FileNotFoundError(f"Secrets file not found at: {secrets_file}")

        with open(secrets_file, 'r', encoding='utf-8') as f:
            self._secrets = yaml.safe_load(f)

    def get_secret(self, provider_name: str) -> Optional[str]:
        """
        Retrieves the API key for a given provider.

        Args:
            provider_name: The name of the provider (e.g., 'openai', 'anthropic').

        Returns:
            The API key as a string, or None if not found.
        """
        return self._secrets.get(provider_name, {}).get('api_key')
import pytest
import yaml
from pathlib import Path
from src.llminventory.secret_manager import SecretManager

@pytest.fixture
def temp_secrets_file(tmp_path):
    """
    Creates a temporary secrets.yaml file for testing.
    """
    secrets_content = {
        "openai": {
            "api_key": "sk-openai-testkey"
        },
        "anthropic": {
            "api_key": "sk-anthropic-testkey"
        },
        "google": {
            "api_key": "google-testkey"
        },
        "mistral": {
            "api_key": "mistral-testkey"
        },
        "cohere": {
            "api_key": "cohere-testkey"
        },
        "provider_without_key": {
            "some_other_setting": "value"
        }
    }
    file_path = tmp_path / "secrets.yaml"
    file_path.write_text(yaml.dump(secrets_content))
    return file_path

@pytest.fixture
def invalid_yaml_file(tmp_path):
    """
    Creates a temporary invalid YAML file for testing error handling.
    """
    file_path = tmp_path / "invalid_secrets.yaml"
    file_path.write_text("key: value\n  - broken_indentation")
    return file_path

def test_secret_manager_loads_secrets_correctly(temp_secrets_file):
    """Test that SecretManager loads secrets from a valid file."""
    manager = SecretManager(temp_secrets_file)
    assert manager.get_secret("openai") == "sk-openai-testkey"
    assert manager.get_secret("anthropic") == "sk-anthropic-testkey"
    assert manager.get_secret("google") == "google-testkey"

def test_secret_manager_handles_file_not_found():
    """Test that SecretManager raises FileNotFoundError for non-existent file."""
    with pytest.raises(FileNotFoundError, match="Secrets file not found at: /non/existent/secrets.yaml"):
        SecretManager(Path("/non/existent/secrets.yaml"))

def test_secret_manager_handles_invalid_yaml(invalid_yaml_file):
    """Test that SecretManager raises YAMLError for invalid YAML content."""
    with pytest.raises(yaml.YAMLError):
        SecretManager(invalid_yaml_file)

def test_get_secret_existing_provider(temp_secrets_file):
    """Test retrieving a secret for an existing provider."""
    manager = SecretManager(temp_secrets_file)
    assert manager.get_secret("mistral") == "mistral-testkey"

def test_get_secret_non_existing_provider(temp_secrets_file):
    """Test retrieving a secret for a non-existing provider returns None."""
    manager = SecretManager(temp_secrets_file)
    assert manager.get_secret("non_existent_provider") is None

def test_get_secret_provider_without_api_key(temp_secrets_file):
    """Test retrieving a secret for a provider that exists but lacks an 'api_key' field."""
    manager = SecretManager(temp_secrets_file)
    assert manager.get_secret("provider_without_key") is None

def test_secret_manager_initialization_without_file():
    """Test that SecretManager can be initialized without a secrets file."""
    manager = SecretManager()
    assert manager.get_secret("openai") is None
    # Attempting to load later should still work
    manager.load_secrets(Path("secrets.example.yaml")) # Using an existing example file for this test
    assert manager.get_secret("openai") == "sk-..." # Based on secrets.example.yaml content
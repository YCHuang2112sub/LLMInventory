import pytest
import yaml
from pathlib import Path
from src.llminventory.model_config_manager import ModelConfigManager

@pytest.fixture
def temp_configs_dir(tmp_path):
    """
    Creates a temporary directory with sample model configuration files.
    """
    configs_dir = tmp_path / "configs"
    configs_dir.mkdir()

    # Valid OpenAI config
    openai_config = {
        "provider": "openai",
        "model": "gpt-4-turbo",
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "description": "OpenAI GPT-4 Turbo",
        "required_fields": ["messages"],
        "parameters": {
            "temperature": {"type": "float", "default": 1.0},
            "max_tokens": {"type": "integer", "default": 4096},
            "top_p": {"type": "float", "default": 1.0},
            "stream": {"type": "boolean", "default": False}
        }
    }
    (configs_dir / "openai_gpt-4-turbo.yaml").write_text(yaml.dump(openai_config))

    # Valid Anthropic config
    anthropic_config = {
        "provider": "anthropic",
        "model": "claude-3-haiku",
        "endpoint": "https://api.anthropic.com/v1/messages",
        "description": "Anthropic Claude 3 Haiku",
        "required_fields": ["messages"],
        "parameters": {
            "max_tokens": {"type": "integer", "default": 1024},
            "temperature": {"type": "float", "default": 1.0}
        }
    }
    (configs_dir / "anthropic_claude-3-haiku.yaml").write_text(yaml.dump(anthropic_config))

    # Invalid YAML file
    (configs_dir / "invalid.yaml").write_text("provider: invalid\n  model: broken")

    # Config with missing required field
    missing_field_config = {
        "provider": "test",
        "model": "missing-desc",
        "endpoint": "http://test.com",
        "required_fields": ["input"],
        "parameters": {}
        # 'description' is missing
    }
    (configs_dir / "missing_field.yaml").write_text(yaml.dump(missing_field_config))

    return configs_dir

def test_init_loads_configs_correctly(temp_configs_dir):
    """Test that ModelConfigManager correctly loads valid configurations."""
    manager = ModelConfigManager(temp_configs_dir)
    assert len(manager.get_all_model_names()) == 2
    assert "openai/gpt-4-turbo" in manager.get_all_model_names()
    assert "anthropic/claude-3-haiku" in manager.get_all_model_names()

def test_init_handles_missing_directory():
    """Test that ModelConfigManager raises NotADirectoryError for non-existent path."""
    with pytest.raises(NotADirectoryError):
        ModelConfigManager(Path("/non/existent/path"))

def test_init_handles_invalid_yaml(temp_configs_dir, capsys):
    """Test that ModelConfigManager logs a warning for invalid YAML files."""
    manager = ModelConfigManager(temp_configs_dir)
    captured = capsys.readouterr()
    assert "Warning: Could not parse YAML file invalid.yaml" in captured.err
    # Ensure it still loads valid configs
    assert len(manager.get_all_model_names()) == 2

def test_init_handles_missing_required_keys(temp_configs_dir, capsys):
    """Test that ModelConfigManager logs a warning for configs missing required top-level keys."""
    manager = ModelConfigManager(temp_configs_dir)
    captured = capsys.readouterr()
    assert "Warning: Invalid config file missing_field.yaml: Missing required fields ['description'] in config" in captured.err
    # Ensure it still loads valid configs
    assert len(manager.get_all_model_names()) == 2

def test_get_model_config_existing(temp_configs_dir):
    """Test retrieving an existing model configuration."""
    manager = ModelConfigManager(temp_configs_dir)
    config = manager.get_model_config("openai", "gpt-4-turbo")
    assert config is not None
    assert config['description'] == "OpenAI GPT-4 Turbo"

def test_get_model_config_non_existing(temp_configs_dir):
    """Test retrieving a non-existing model configuration returns None."""
    manager = ModelConfigManager(temp_configs_dir)
    config = manager.get_model_config("nonexistent", "model")
    assert config is None

def test_get_all_model_names(temp_configs_dir):
    """Test that get_all_model_names returns all loaded model keys."""
    manager = ModelConfigManager(temp_configs_dir)
    names = manager.get_all_model_names()
    assert sorted(names) == ["anthropic/claude-3-haiku", "openai/gpt-4-turbo"]

def test_merge_and_validate_params_defaults(temp_configs_dir):
    """Test merging parameters with only defaults, no user overrides."""
    manager = ModelConfigManager(temp_configs_dir)
    merged_params = manager.merge_and_validate_params("openai", "gpt-4-turbo")
    assert merged_params == {
        "temperature": 1.0,
        "max_tokens": 4096,
        "top_p": 1.0,
        "stream": False
    }

def test_merge_and_validate_params_user_overrides(temp_configs_dir):
    """Test merging parameters with user overrides."""
    manager = ModelConfigManager(temp_configs_dir)
    user_params = {"temperature": 0.7, "max_tokens": 100}
    merged_params = manager.merge_and_validate_params("openai", "gpt-4-turbo", user_params)
    assert merged_params == {
        "temperature": 0.7,
        "max_tokens": 100,
        "top_p": 1.0,
        "stream": False
    }

def test_merge_and_validate_params_type_validation_float(temp_configs_dir):
    """Test float type validation."""
    manager = ModelConfigManager(temp_configs_dir)
    user_params = {"temperature": 0.5}
    merged_params = manager.merge_and_validate_params("openai", "gpt-4-turbo", user_params)
    assert merged_params["temperature"] == 0.5
    assert isinstance(merged_params["temperature"], float)

def test_merge_and_validate_params_type_validation_integer(temp_configs_dir):
    """Test integer type validation."""
    manager = ModelConfigManager(temp_configs_dir)
    user_params = {"max_tokens": 512}
    merged_params = manager.merge_and_validate_params("openai", "gpt-4-turbo", user_params)
    assert merged_params["max_tokens"] == 512
    assert isinstance(merged_params["max_tokens"], int)

def test_merge_and_validate_params_type_validation_boolean(temp_configs_dir):
    """Test boolean type validation."""
    manager = ModelConfigManager(temp_configs_dir)
    user_params = {"stream": True}
    merged_params = manager.merge_and_validate_params("openai", "gpt-4-turbo", user_params)
    assert merged_params["stream"] is True
    assert isinstance(merged_params["stream"], bool)

def test_merge_and_validate_params_int_to_float_conversion(temp_configs_dir):
    """Test that integers are correctly converted to floats if expected type is float."""
    manager = ModelConfigManager(temp_configs_dir)
    user_params = {"temperature": 1} # User provides an int for a float param
    merged_params = manager.merge_and_validate_params("openai", "gpt-4-turbo", user_params)
    assert merged_params["temperature"] == 1.0
    assert isinstance(merged_params["temperature"], float)

def test_merge_and_validate_params_ignores_unsupported(temp_configs_dir):
    """Test that unsupported parameters provided by the user are ignored."""
    manager = ModelConfigManager(temp_configs_dir)
    user_params = {"temperature": 0.5, "unsupported_param": "value"}
    merged_params = manager.merge_and_validate_params("openai", "gpt-4-turbo", user_params)
    assert "unsupported_param" not in merged_params
    assert merged_params["temperature"] == 0.5

def test_merge_and_validate_params_raises_value_error_for_invalid_type(temp_configs_dir):
    """Test that ValueError is raised for type mismatch."""
    manager = ModelConfigManager(temp_configs_dir)
    user_params = {"temperature": "high"} # Expected float, got string
    with pytest.raises(ValueError, match="expected type 'float', but got 'str'"):
        manager.merge_and_validate_params("openai", "gpt-4-turbo", user_params)

    user_params = {"max_tokens": 100.5} # Expected integer, got float
    with pytest.raises(ValueError, match="expected type 'integer', but got 'float'"):
        manager.merge_and_validate_params("openai", "gpt-4-turbo", user_params)

def test_merge_and_validate_params_raises_key_error_for_missing_model(temp_configs_dir):
    """Test that KeyError is raised if the specified model is not found."""
    manager = ModelConfigManager(temp_configs_dir)
    with pytest.raises(KeyError, match="Model 'nonexistent/model' not found in configurations."):
        manager.merge_and_validate_params("nonexistent", "model", {"temperature": 0.5})
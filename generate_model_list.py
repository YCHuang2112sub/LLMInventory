"""
Scans the 'configs/' directory to automatically generate:
- supported_models.json: A JSON list of all model configurations.
- supported_models.yaml: A YAML list of all model configurations.
- MODELS.md: Human-readable documentation for all supported models.

This script should be run every time a model configuration is added,
updated, or removed to keep the project's documentation in sync.
"""

import json
import yaml
from pathlib import Path
from collections import defaultdict

def generate_model_lists():
    """
    Scans model configs and generates JSON, YAML, and Markdown documentation.
    """
    project_root = Path(__file__).parent
    configs_dir = project_root / "configs"
    
    if not configs_dir.is_dir():
        print(f"Error: Configs directory not found at '{configs_dir}'")
        return

    all_models = []
    for config_file in sorted(configs_dir.glob("*.yaml")):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                # Basic validation
                if not all(k in config for k in ['provider', 'model', 'description']):
                    print(f"Warning: Skipping invalid config file {config_file.name}, missing required keys.")
                    continue
                all_models.append(config)
        except yaml.YAMLError as e:
            print(f"Warning: Could not parse YAML file {config_file.name}: {e}")

    # --- Generate supported_models.json ---
    json_output_path = project_root / "supported_models.json"
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(all_models, f, indent=2)
    print(f"Successfully generated {json_output_path}")

    # --- Generate supported_models.yaml ---
    yaml_output_path = project_root / "supported_models.yaml"
    with open(yaml_output_path, 'w', encoding='utf-8') as f:
        yaml.dump(all_models, f, sort_keys=False, default_flow_style=False)
    print(f"Successfully generated {yaml_output_path}")

    # --- Generate MODELS.md ---
    md_output_path = project_root / "MODELS.md"
    generate_markdown_docs(all_models, md_output_path)
    print(f"Successfully generated {md_output_path}")

def generate_markdown_docs(models: list, output_path: Path):
    """Generates the MODELS.md file from the list of model configs."""
    
    # Group models by provider
    models_by_provider = defaultdict(list)
    for model in models:
        models_by_provider[model['provider']].append(model)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Supported Models\n\n")
        f.write("This document lists all models supported by the LLMInventory API. ")
        f.write("It is automatically generated from the configuration files in the `configs/` directory.\n\n")
        f.write("--- \n\n")

        for provider in sorted(models_by_provider.keys()):
            f.write(f"## {provider.capitalize()}\n\n")
            
            for model in sorted(models_by_provider[provider], key=lambda m: m['model']):
                model_id = f"{model['provider']}/{model['model']}"
                f.write(f"### `{model_id}`\n\n")
                f.write(f"{model['description']}\n\n")

                # Parameters table
                if model.get('parameters'):
                    f.write("**Parameters:**\n\n")
                    f.write("| Parameter | Type | Default | Description |\n")
                    f.write("|---|---|---|---|\n")
                    for param_name, param_info in model['parameters'].items():
                        p_type = param_info.get('type', 'N/A')
                        p_default = param_info.get('default', 'N/A')
                        p_desc = param_info.get('description', 'No description available.')
                        f.write(f"| `{param_name}` | `{p_type}` | `{p_default}` | {p_desc} |\n")
                    f.write("\n")

                # Required Fields
                if model.get('required_fields'):
                    f.write("**Required Payload Fields:**\n\n")
                    for field in model['required_fields']:
                        f.write(f"- `{field}`\n")
                    f.write("\n")

            f.write("---\n\n")

if __name__ == "__main__":
    generate_model_lists()
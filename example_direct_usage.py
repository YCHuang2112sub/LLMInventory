"""
An example script demonstrating how to use the LLMInventory programmatically
without running the FastAPI server.
"""

from pathlib import Path
from src.llminventory import LLMInventory
import json  

def main():
    """Main function to demonstrate direct usage."""
    print("--- Initializing LLMInventory ---")
    
    # Define paths relative to this script
    project_root = Path(__file__).parent
    configs_dir = project_root / "configs"
    secrets_file = project_root / "secrets.yaml"
    
    try:
        # Create an instance of the inventory
        inventory = LLMInventory(configs_dir=configs_dir, secrets_file=secrets_file)
    except Exception as e:
        print(f"Failed to initialize LLMInventory: {e}")
        return

    # --- 1. List all supported models ---
    print("\n--- 1. Listing all supported models ---")
    supported_models = inventory.get_supported_models()
    print(f"Found {len(supported_models)} supported models.")
    for model_info in supported_models:
        print(f"  - {model_info['provider']}/{model_info['model']}")

    # --- 2. Invoke an OpenAI model ---
    print("\n--- 2. Invoking OpenAI's gpt-4o ---")
    try:
        openai_payload = {
            "messages": [
                {"role": "user", "content": "Hello, what is the capital of France?"}
            ]
        }
        openai_params = {
            "temperature": 0.5
        }
        
        response = inventory.invoke(
            provider="openai",
            model="gpt-4o",
            payload=openai_payload,
            parameters=openai_params
        )
        
        print("OpenAI Response:")
        # Pretty-print the JSON response
        print(json.dumps(response, indent=2))
        
    except (KeyError, ValueError, ConnectionError) as e:
        print(f"Error invoking OpenAI model: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # --- 3. Invoke an Anthropic model ---
    print("\n--- 3. Invoking Anthropic's claude-3-sonnet ---")
    try:
        anthropic_payload = {
            "messages": [
                {"role": "user", "content": "What are the main benefits of using Python?"}
            ]
        }
        
        response = inventory.invoke(
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            payload=anthropic_payload
            # No parameters, so defaults will be used
        )
        
        print("Anthropic Response:")
        print(json.dumps(response, indent=2))
        
    except (KeyError, ValueError, ConnectionError) as e:
        print(f"Error invoking Anthropic model: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # --- 4. Invoke a Google model ---
    print("\n--- 4. Invoking Google's gemini-1.5-pro-latest ---")
    try:
        # Note: Google's API uses a different payload structure
        google_payload = {
            "contents": [{
                "parts": [{"text": "Explain the concept of zero-shot learning in simple terms."}]
            }]
        }

        response = inventory.invoke(
            provider="google",
            model="gemini-1.5-pro-latest",
            payload=google_payload
        )

        print("Google Response:")
        print(json.dumps(response, indent=2))

    except (KeyError, ValueError, ConnectionError) as e:
        print(f"Error invoking Google model: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
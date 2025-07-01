"""
Interactive testing script for LLM models.
Allows you to test models with custom prompts easily.
"""

import json
import time
from pathlib import Path
from src.llminventory import LLMInventory


def get_available_models(inventory):
    """Get list of available models grouped by provider."""
    try:
        models = inventory.get_supported_models()
        providers = {}
        
        for model in models:
            provider = model['provider']
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(model['model'])
        
        return providers
    except Exception as e:
        print(f"❌ Error getting models: {e}")
        return {}


def test_model_interactive(inventory, provider, model, prompt, max_tokens=200, temperature=0.7):
    """Test a model with custom prompt."""
    try:
        # Prepare payload based on provider
        if provider == "google":
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            params = {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        else:
            payload = {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            params = {
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        
        print(f"🚀 Testing {provider}/{model}...")
        start_time = time.time()
        
        response = inventory.invoke(
            provider=provider,
            model=model,
            payload=payload,
            parameters=params
        )
        
        end_time = time.time()
        
        # Extract response text based on provider
        if provider == "google":
            candidates = response.get("candidates", [])
            response_text = "No response"
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts and "text" in parts[0]:
                    response_text = parts[0]["text"]
        elif provider == "anthropic":
            response_text = response.get("content", [{}])[0].get("text", "No response")
        else:  # OpenAI, xAI, Mistral
            response_text = response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        
        # Print results
        print(f"✅ Success ({end_time - start_time:.2f}s)")
        print(f"\n📄 Response:")
        print("-" * 50)
        print(response_text)
        print("-" * 50)
        
        # Show usage info if available
        usage = response.get("usage", response.get("usageMetadata", {}))
        if usage:
            print(f"\n📊 Usage: {usage}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def main():
    """Main interactive testing function."""
    print("🤖 LLM Interactive Tester")
    print("=" * 50)
    
    # Initialize inventory
    project_root = Path(__file__).parent
    configs_dir = project_root / "configs"
    secrets_file = project_root / "secrets.yaml"
    
    try:
        inventory = LLMInventory(configs_dir=configs_dir, secrets_file=secrets_file)
        print("✅ LLMInventory initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize LLMInventory: {e}")
        return
    
    # Get available models
    providers = get_available_models(inventory)
    
    if not providers:
        print("❌ No models available")
        return
    
    while True:
        print("\n🔍 Available Providers:")
        for i, (provider, models) in enumerate(providers.items(), 1):
            print(f"  {i}. {provider} ({len(models)} models)")
        
        print("  0. Exit")
        
        try:
            choice = input("\nSelect provider (number): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            
            provider_idx = int(choice) - 1
            provider_list = list(providers.keys())
            
            if 0 <= provider_idx < len(provider_list):
                selected_provider = provider_list[provider_idx]
                models = providers[selected_provider]
                
                print(f"\n📋 Available models for {selected_provider}:")
                for i, model in enumerate(models, 1):
                    print(f"  {i}. {model}")
                
                model_choice = input(f"\nSelect model (1-{len(models)}): ").strip()
                model_idx = int(model_choice) - 1
                
                if 0 <= model_idx < len(models):
                    selected_model = models[model_idx]
                    
                    print(f"\n🎯 Selected: {selected_provider}/{selected_model}")
                    
                    # Get prompt from user
                    prompt = input("\n💬 Enter your prompt: ").strip()
                    
                    if prompt:
                        # Optional parameters
                        print("\n⚙️ Optional parameters (press Enter for defaults):")
                        
                        max_tokens_input = input("Max tokens (default: 200): ").strip()
                        max_tokens = int(max_tokens_input) if max_tokens_input else 200
                        
                        temp_input = input("Temperature (default: 0.7): ").strip()
                        temperature = float(temp_input) if temp_input else 0.7
                        
                        # Test the model
                        print("\n" + "=" * 60)
                        test_model_interactive(
                            inventory, 
                            selected_provider, 
                            selected_model, 
                            prompt, 
                            max_tokens, 
                            temperature
                        )
                        print("=" * 60)
                        
                        # Ask if user wants to continue
                        continue_choice = input("\n🔄 Test another model? (y/N): ").strip().lower()
                        if continue_choice != 'y':
                            print("👋 Goodbye!")
                            break
                    else:
                        print("❌ No prompt provided")
                else:
                    print("❌ Invalid model selection")
            else:
                print("❌ Invalid provider selection")
                
        except (ValueError, KeyboardInterrupt):
            if KeyboardInterrupt:
                print("\n👋 Goodbye!")
            else:
                print("❌ Invalid input")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 
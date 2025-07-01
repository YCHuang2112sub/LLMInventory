"""
Script to test a single provider with specific models.
Usage: python test_single_provider.py <provider> [model]
"""

import sys
import json
import time
from pathlib import Path
from src.llminventory import LLMInventory


def test_provider(provider_name: str, model_name: str = None):
    """Test a specific provider and optionally a specific model."""
    
    # Initialize inventory
    project_root = Path(__file__).parent
    configs_dir = project_root / "configs"
    secrets_file = project_root / "secrets.yaml"
    
    try:
        inventory = LLMInventory(configs_dir=configs_dir, secrets_file=secrets_file)
        print(f"✅ LLMInventory initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize LLMInventory: {e}")
        return False
    
    # Get supported models for the provider
    try:
        supported_models = inventory.get_supported_models()
        provider_models = [m for m in supported_models if m['provider'] == provider_name]
        
        if not provider_models:
            print(f"❌ No models found for provider: {provider_name}")
            print(f"Available providers: {list(set(m['provider'] for m in supported_models))}")
            return False
        
        print(f"📋 Found {len(provider_models)} models for {provider_name}")
        
    except Exception as e:
        print(f"❌ Error getting supported models: {e}")
        return False
    
    # Determine which models to test
    if model_name:
        models_to_test = [model_name] if model_name in [m['model'] for m in provider_models] else []
        if not models_to_test:
            print(f"❌ Model {model_name} not found for provider {provider_name}")
            print(f"Available models: {[m['model'] for m in provider_models]}")
            return False
    else:
        # Test a few representative models
        models_to_test = [m['model'] for m in provider_models[:3]]  # Test first 3 models
    
    print(f"🧪 Testing {len(models_to_test)} model(s): {models_to_test}")
    
    # Test each model
    results = {}
    for model in models_to_test:
        print(f"\n📝 Testing {provider_name}/{model}...")
        
        try:
            # Get model configuration to check capabilities
            model_config = next((m for m in provider_models if m['model'] == model), None)
            is_embedding_model = model_config and 'embeddings' in model_config.get('capabilities', [])
            
            # Prepare payload based on provider and model type
            if is_embedding_model:
                payload = {
                    "input": "Hello! This is a test sentence for text embedding."
                }
                params = {"dimensions": 768}
            elif provider_name == "google":
                payload = {
                    "contents": [{
                        "parts": [{"text": "Hello! Please respond with a brief greeting and tell me what model you are."}]
                    }]
                }
                params = {"temperature": 0.7, "maxOutputTokens": 100}
            else:
                payload = {
                    "messages": [
                        {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me what model you are."}
                    ]
                }
                params = {"temperature": 0.7, "max_tokens": 100}
            
            # Make the API call
            start_time = time.time()
            response = inventory.invoke(
                provider=provider_name,
                model=model,
                payload=payload,
                parameters=params
            )
            end_time = time.time()
            
            # Extract response text based on provider and model type
            if is_embedding_model:
                if "embedding" in response and "values" in response["embedding"]:
                    embedding_values = response["embedding"]["values"]
                    dimensions = len(embedding_values)
                    response_text = f"Embedding vector with {dimensions} dimensions (first 5 values: {embedding_values[:5]})"
                else:
                    response_text = "No embedding in response"
            elif provider_name == "google":
                candidates = response.get("candidates", [])
                response_text = "No response"
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        response_text = parts[0]["text"]
            elif provider_name == "anthropic":
                response_text = response.get("content", [{}])[0].get("text", "No response")
            else:  # OpenAI, xAI, Mistral
                response_text = response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            
            results[model] = {
                "status": "✅ Success",
                "response_time": f"{end_time - start_time:.2f}s",
                "response": response_text,
                "usage": response.get("usage", response.get("usageMetadata", {}))
            }
            
            print(f"   ✅ Success ({end_time - start_time:.2f}s)")
            print(f"   📄 Response: {response_text[:100]}{'...' if len(response_text) > 100 else ''}")
            
        except Exception as e:
            results[model] = {
                "status": "❌ Failed",
                "error": str(e)
            }
            print(f"   ❌ Failed: {e}")
        
        time.sleep(1)  # Rate limiting
    
    # Print summary
    print(f"\n📊 SUMMARY FOR {provider_name.upper()}")
    print("=" * 50)
    
    successful = sum(1 for r in results.values() if "✅" in r.get("status", ""))
    total = len(results)
    
    for model, result in results.items():
        status = result.get("status", "❌ Unknown")
        response_time = result.get("response_time", "N/A")
        print(f"  {model}: {status} ({response_time})")
    
    print(f"\n📈 Results: {successful}/{total} successful ({successful/total*100:.1f}%)")
    
    # Save results
    results_file = f"test_results_{provider_name}.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"💾 Detailed results saved to {results_file}")
    
    return successful > 0


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python test_single_provider.py <provider> [model]")
        print("\nAvailable providers: openai, anthropic, google, xai, mistral")
        print("\nExamples:")
        print("  python test_single_provider.py openai")
        print("  python test_single_provider.py anthropic claude-3-5-haiku-20241022")
        return 1
    
    provider = sys.argv[1].lower()
    model = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🚀 Testing {provider}" + (f"/{model}" if model else ""))
    print("=" * 50)
    
    success = test_provider(provider, model)
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 
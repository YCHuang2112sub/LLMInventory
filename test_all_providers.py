"""
Comprehensive testing script for all LLM providers.
Tests models from each provider using configured API keys.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any
from src.llminventory import LLMInventory


class ProviderTester:
    """Test models from different providers."""
    
    def __init__(self):
        """Initialize the tester with LLMInventory."""
        project_root = Path(__file__).parent
        configs_dir = project_root / "configs"
        secrets_file = project_root / "secrets.yaml"
        
        try:
            self.inventory = LLMInventory(configs_dir=configs_dir, secrets_file=secrets_file)
            print("✅ LLMInventory initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize LLMInventory: {e}")
            raise
    
    def test_openai_models(self) -> Dict[str, Any]:
        """Test OpenAI models."""
        print("\n🔵 Testing OpenAI Models")
        print("=" * 50)
        
        models_to_test = [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
        
        results = {}
        
        for model in models_to_test:
            print(f"\n📝 Testing {model}...")
            try:
                payload = {
                    "messages": [
                        {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me what model you are."}
                    ]
                }
                
                params = {
                    "temperature": 0.7,
                    "max_tokens": 100
                }
                
                start_time = time.time()
                response = self.inventory.invoke(
                    provider="openai",
                    model=model,
                    payload=payload,
                    parameters=params
                )
                end_time = time.time()
                
                # Extract the response text
                response_text = response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
                
                results[model] = {
                    "status": "✅ Success",
                    "response_time": f"{end_time - start_time:.2f}s",
                    "response": response_text,
                    "usage": response.get("usage", {})
                }
                
                print(f"   ✅ Success ({end_time - start_time:.2f}s)")
                print(f"   📄 Response: {response_text[:100]}...")
                
            except Exception as e:
                results[model] = {
                    "status": "❌ Failed",
                    "error": str(e)
                }
                print(f"   ❌ Failed: {e}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def test_anthropic_models(self) -> Dict[str, Any]:
        """Test Anthropic models."""
        print("\n🟠 Testing Anthropic Models")
        print("=" * 50)
        
        models_to_test = [
            "claude-3-5-haiku-20241022",
            "claude-3-5-sonnet-20241022",
            "claude-3-haiku-20240307"
        ]
        
        results = {}
        
        for model in models_to_test:
            print(f"\n📝 Testing {model}...")
            try:
                payload = {
                    "messages": [
                        {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me what model you are."}
                    ]
                }
                
                params = {
                    "temperature": 0.7,
                    "max_tokens": 100
                }
                
                start_time = time.time()
                response = self.inventory.invoke(
                    provider="anthropic",
                    model=model,
                    payload=payload,
                    parameters=params
                )
                end_time = time.time()
                
                # Extract the response text
                response_text = response.get("content", [{}])[0].get("text", "No response")
                
                results[model] = {
                    "status": "✅ Success",
                    "response_time": f"{end_time - start_time:.2f}s",
                    "response": response_text,
                    "usage": response.get("usage", {})
                }
                
                print(f"   ✅ Success ({end_time - start_time:.2f}s)")
                print(f"   📄 Response: {response_text[:100]}...")
                
            except Exception as e:
                results[model] = {
                    "status": "❌ Failed",
                    "error": str(e)
                }
                print(f"   ❌ Failed: {e}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def test_google_models(self) -> Dict[str, Any]:
        """Test Google models."""
        print("\n🔴 Testing Google Models")
        print("=" * 50)
        
        models_to_test = [
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro-latest",
            "gemini-2.0-flash-exp"
        ]
        
        results = {}
        
        for model in models_to_test:
            print(f"\n📝 Testing {model}...")
            try:
                payload = {
                    "contents": [{
                        "parts": [{"text": "Hello! Please respond with a brief greeting and tell me what model you are."}]
                    }]
                }
                
                params = {
                    "temperature": 0.7,
                    "maxOutputTokens": 100
                }
                
                start_time = time.time()
                response = self.inventory.invoke(
                    provider="google",
                    model=model,
                    payload=payload,
                    parameters=params
                )
                end_time = time.time()
                
                # Extract the response text
                candidates = response.get("candidates", [])
                response_text = "No response"
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        response_text = parts[0]["text"]
                
                results[model] = {
                    "status": "✅ Success",
                    "response_time": f"{end_time - start_time:.2f}s",
                    "response": response_text,
                    "usage": response.get("usageMetadata", {})
                }
                
                print(f"   ✅ Success ({end_time - start_time:.2f}s)")
                print(f"   📄 Response: {response_text[:100]}...")
                
            except Exception as e:
                results[model] = {
                    "status": "❌ Failed",
                    "error": str(e)
                }
                print(f"   ❌ Failed: {e}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def test_xai_models(self) -> Dict[str, Any]:
        """Test xAI models."""
        print("\n⚫ Testing xAI Models")
        print("=" * 50)
        
        models_to_test = [
            "grok-2-mini",
            "grok-2",
            "grok-beta"
        ]
        
        results = {}
        
        for model in models_to_test:
            print(f"\n📝 Testing {model}...")
            try:
                payload = {
                    "messages": [
                        {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me what model you are."}
                    ]
                }
                
                params = {
                    "temperature": 0.7,
                    "max_tokens": 100
                }
                
                start_time = time.time()
                response = self.inventory.invoke(
                    provider="xai",
                    model=model,
                    payload=payload,
                    parameters=params
                )
                end_time = time.time()
                
                # Extract the response text
                response_text = response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
                
                results[model] = {
                    "status": "✅ Success",
                    "response_time": f"{end_time - start_time:.2f}s",
                    "response": response_text,
                    "usage": response.get("usage", {})
                }
                
                print(f"   ✅ Success ({end_time - start_time:.2f}s)")
                print(f"   📄 Response: {response_text[:100]}...")
                
            except Exception as e:
                results[model] = {
                    "status": "❌ Failed",
                    "error": str(e)
                }
                print(f"   ❌ Failed: {e}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def test_mistral_models(self) -> Dict[str, Any]:
        """Test Mistral models."""
        print("\n🟡 Testing Mistral Models")
        print("=" * 50)
        
        models_to_test = [
            "mistral-large-2411",
            "ministral-8b-2410",
            "pixtral-12b-2409"
        ]
        
        results = {}
        
        for model in models_to_test:
            print(f"\n📝 Testing {model}...")
            try:
                payload = {
                    "messages": [
                        {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me what model you are."}
                    ]
                }
                
                params = {
                    "temperature": 0.7,
                    "max_tokens": 100
                }
                
                start_time = time.time()
                response = self.inventory.invoke(
                    provider="mistral",
                    model=model,
                    payload=payload,
                    parameters=params
                )
                end_time = time.time()
                
                # Extract the response text
                response_text = response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
                
                results[model] = {
                    "status": "✅ Success",
                    "response_time": f"{end_time - start_time:.2f}s",
                    "response": response_text,
                    "usage": response.get("usage", {})
                }
                
                print(f"   ✅ Success ({end_time - start_time:.2f}s)")
                print(f"   📄 Response: {response_text[:100]}...")
                
            except Exception as e:
                results[model] = {
                    "status": "❌ Failed",
                    "error": str(e)
                }
                print(f"   ❌ Failed: {e}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run tests for all providers."""
        print("🚀 Starting Comprehensive Provider Testing")
        print("=" * 60)
        
        all_results = {}
        
        # Test each provider
        try:
            all_results["openai"] = self.test_openai_models()
        except Exception as e:
            print(f"❌ OpenAI testing failed: {e}")
            all_results["openai"] = {"error": str(e)}
        
        try:
            all_results["anthropic"] = self.test_anthropic_models()
        except Exception as e:
            print(f"❌ Anthropic testing failed: {e}")
            all_results["anthropic"] = {"error": str(e)}
        
        try:
            all_results["google"] = self.test_google_models()
        except Exception as e:
            print(f"❌ Google testing failed: {e}")
            all_results["google"] = {"error": str(e)}
        
        try:
            all_results["xai"] = self.test_xai_models()
        except Exception as e:
            print(f"❌ xAI testing failed: {e}")
            all_results["xai"] = {"error": str(e)}
        
        try:
            all_results["mistral"] = self.test_mistral_models()
        except Exception as e:
            print(f"❌ Mistral testing failed: {e}")
            all_results["mistral"] = {"error": str(e)}
        
        return all_results
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a summary of all test results."""
        print("\n📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        successful_tests = 0
        
        for provider, provider_results in results.items():
            if "error" in provider_results:
                print(f"\n❌ {provider.upper()}: Provider failed to initialize")
                continue
            
            print(f"\n{provider.upper()}:")
            for model, result in provider_results.items():
                total_tests += 1
                status = result.get("status", "❌ Unknown")
                if "✅" in status:
                    successful_tests += 1
                
                response_time = result.get("response_time", "N/A")
                print(f"  {model}: {status} ({response_time})")
        
        print(f"\n📈 OVERALL RESULTS:")
        print(f"   Total tests: {total_tests}")
        print(f"   Successful: {successful_tests}")
        print(f"   Failed: {total_tests - successful_tests}")
        print(f"   Success rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "   Success rate: 0%")
        
        # Save results to file
        with open("test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Detailed results saved to test_results.json")


def main():
    """Main function to run provider tests."""
    try:
        tester = ProviderTester()
        results = tester.run_all_tests()
        tester.print_summary(results)
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 
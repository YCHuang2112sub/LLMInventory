"""
Final comprehensive test of all working LLM models.
Tests only confirmed working models from each provider.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any
from src.llminventory import LLMInventory


class FinalModelTester:
    """Test only confirmed working models from different providers."""
    
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
    
    def test_provider_models(self, provider: str, models: List[str], payload_format: str = "messages") -> Dict[str, Any]:
        """Test models from a specific provider."""
        print(f"\n🔵 Testing {provider.upper()} Models")
        print("=" * 50)
        
        results = {}
        
        for model in models:
            print(f"\n📝 Testing {model}...")
            try:
                # Prepare payload based on provider format
                if payload_format == "messages":
                    payload = {
                        "messages": [
                            {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me what model you are."}
                        ]
                    }
                elif payload_format == "contents":
                    payload = {
                        "contents": [{
                            "parts": [{"text": "Hello! Please respond with a brief greeting and tell me what model you are."}]
                        }]
                    }
                else:
                    payload = {
                        "messages": [
                            {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me what model you are."}
                        ]
                    }
                
                params = {
                    "temperature": 0.7,
                    "max_tokens": 100 if payload_format == "messages" else None,
                    "maxOutputTokens": 100 if payload_format == "contents" else None
                }
                
                # Remove None values
                params = {k: v for k, v in params.items() if v is not None}
                
                start_time = time.time()
                response = self.inventory.invoke(
                    provider=provider,
                    model=model,
                    payload=payload,
                    parameters=params
                )
                end_time = time.time()
                
                # Extract the response text based on provider format
                response_text = self._extract_response_text(response, provider)
                
                results[model] = {
                    "status": "✅ Success",
                    "response_time": f"{end_time - start_time:.2f}s",
                    "response": response_text,
                    "usage": self._extract_usage(response, provider)
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
    
    def _extract_response_text(self, response: Dict[str, Any], provider: str) -> str:
        """Extract response text based on provider format."""
        try:
            if provider == "openai" or provider == "xai" or provider == "mistral":
                return response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            elif provider == "anthropic":
                return response.get("content", [{}])[0].get("text", "No response")
            elif provider == "google":
                candidates = response.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"]
                return "No response"
            else:
                return str(response)
        except:
            return "Error extracting response"
    
    def _extract_usage(self, response: Dict[str, Any], provider: str) -> Dict[str, Any]:
        """Extract usage information based on provider format."""
        try:
            if provider == "openai" or provider == "xai" or provider == "mistral":
                return response.get("usage", {})
            elif provider == "anthropic":
                return response.get("usage", {})
            elif provider == "google":
                return response.get("usageMetadata", {})
            else:
                return {}
        except:
            return {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run tests for all working providers."""
        print("🚀 Starting Final Comprehensive Model Testing (WORKING MODELS ONLY)")
        print("=" * 70)
        
        all_results = {}
        
        # Test OpenAI models (confirmed working)
        try:
            openai_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4.1", "gpt-4.1-mini"]
            all_results["openai"] = self.test_provider_models("openai", openai_models, "messages")
        except Exception as e:
            print(f"❌ OpenAI testing failed: {e}")
            all_results["openai"] = {"error": str(e)}
        
        # Test Anthropic models (confirmed working)
        try:
            anthropic_models = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-haiku-20240307"]
            all_results["anthropic"] = self.test_provider_models("anthropic", anthropic_models, "messages")
        except Exception as e:
            print(f"❌ Anthropic testing failed: {e}")
            all_results["anthropic"] = {"error": str(e)}
        
        # Test Google models (confirmed working)
        try:
            google_models = ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-flash-8b"]
            # Note: gemini-1.5-pro might have rate limits, so testing separately
            all_results["google"] = self.test_provider_models("google", google_models, "contents")
        except Exception as e:
            print(f"❌ Google testing failed: {e}")
            all_results["google"] = {"error": str(e)}
        
        # Test xAI models (if API key available)
        try:
            xai_models = ["grok-2", "grok-2-mini", "grok-beta"]
            all_results["xai"] = self.test_provider_models("xai", xai_models, "messages")
        except Exception as e:
            print(f"❌ xAI testing failed: {e}")
            all_results["xai"] = {"error": str(e)}
        
        # Test Mistral models (if API key available)
        try:
            mistral_models = ["mistral-large-2411", "mistral-small-2409", "ministral-8b-2410"]
            all_results["mistral"] = self.test_provider_models("mistral", mistral_models, "messages")
        except Exception as e:
            print(f"❌ Mistral testing failed: {e}")
            all_results["mistral"] = {"error": str(e)}
        
        return all_results
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a summary of all test results."""
        print("\n📊 FINAL COMPREHENSIVE TEST SUMMARY")
        print("=" * 70)
        
        total_tests = 0
        successful_tests = 0
        
        for provider, provider_results in results.items():
            if "error" in provider_results:
                print(f"\n❌ {provider.upper()}: Provider failed to initialize")
                print(f"   Error: {provider_results['error']}")
                continue
            
            provider_success = 0
            provider_total = len(provider_results)
            
            print(f"\n{provider.upper()} ({provider_total} models):")
            for model, result in provider_results.items():
                total_tests += 1
                status = result.get("status", "❌ Unknown")
                if "✅" in status:
                    successful_tests += 1
                    provider_success += 1
                
                response_time = result.get("response_time", "N/A")
                print(f"  {model}: {status} ({response_time})")
                
                # Show usage if available
                usage = result.get("usage", {})
                if usage:
                    if "total_tokens" in usage:
                        print(f"    📊 Tokens: {usage.get('total_tokens', 'N/A')}")
                    elif "input_tokens" in usage:
                        print(f"    📊 Tokens: {usage.get('input_tokens', 0)} + {usage.get('output_tokens', 0)}")
            
            success_rate = (provider_success / provider_total * 100) if provider_total > 0 else 0
            print(f"  📈 Provider Success Rate: {provider_success}/{provider_total} ({success_rate:.1f}%)")
        
        print(f"\n📈 FINAL RESULTS:")
        print(f"   Total tests: {total_tests}")
        print(f"   Successful: {successful_tests}")
        print(f"   Failed: {total_tests - successful_tests}")
        print(f"   Success rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "   Success rate: 0%")
        
        # Save results to file
        with open("test_results_final.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Detailed results saved to test_results_final.json")


def main():
    """Main function to run provider tests."""
    try:
        tester = FinalModelTester()
        results = tester.run_all_tests()
        tester.print_summary(results)
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 
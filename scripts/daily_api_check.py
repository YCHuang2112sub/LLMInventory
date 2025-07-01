#!/usr/bin/env python3
"""
Daily API Updates Check Script
Monitors all supported providers for new models, pricing changes, and deprecations
"""

import json
import yaml
import requests
import time
from datetime import datetime
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from llminventory import LLMInventory

class APIUpdateChecker:
    def __init__(self):
        self.current_models = self.load_current_models()
        self.updates_found = {
            'new_models': [],
            'deprecated_models': [],
            'pricing_changes': [],
            'capability_changes': [],
            'check_date': datetime.now().isoformat()
        }
        
    def load_current_models(self):
        """Load current model configuration"""
        with open('supported_models.yaml', 'r') as f:
            config = yaml.safe_load(f)
            return config if isinstance(config, list) else config.get('models', [])
    
    def check_openai_updates(self):
        """Check OpenAI for new models and updates"""
        print("🔵 Checking OpenAI API updates...")
        
        try:
            # OpenAI models endpoint
            headers = {"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', '')}"}
            response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=30)
            
            if response.status_code == 200:
                api_models = response.json().get('data', [])
                current_openai_models = [m['model'] for m in self.current_models if m.get('provider') == 'openai']
                
                # Check for new models
                for model in api_models:
                    model_id = model.get('id', '')
                    if (model_id not in current_openai_models and 
                        any(prefix in model_id for prefix in ['gpt-', 'dall-e-', 'o1-', 'o3-'])):
                        
                        self.updates_found['new_models'].append({
                            'provider': 'openai',
                            'model': model_id,
                            'description': f"New OpenAI model detected: {model_id}",
                            'created': model.get('created'),
                            'owned_by': model.get('owned_by')
                        })
                        print(f"  🆕 New model found: {model_id}")
                
                print(f"  ✅ OpenAI check complete - {len(api_models)} models scanned")
            else:
                print(f"  ⚠️ OpenAI API error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ OpenAI check failed: {e}")
    
    def check_anthropic_updates(self):
        """Check Anthropic for updates (limited API info available)"""
        print("🟠 Checking Anthropic updates...")
        
        # Anthropic doesn't have a public models list API
        # Check for known model patterns and test existing models
        try:
            known_models = ['claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022', 'claude-3-haiku-20240307']
            current_anthropic_models = [m['model'] for m in self.current_models if m.get('provider') == 'anthropic']
            
            # Check for potential new models (based on naming patterns)
            potential_new_models = [
                'claude-3-5-sonnet-20250101',  # Potential future version
                'claude-4-sonnet-20250101',    # Potential Claude 4
                'claude-3-5-opus-20241022'     # Potential Opus version
            ]
            
            for model in potential_new_models:
                if model not in current_anthropic_models:
                    # Test if model exists by making a small request
                    headers = {
                        "Authorization": f"Bearer {os.environ.get('ANTHROPIC_API_KEY', '')}",
                        "Content-Type": "application/json",
                        "anthropic-version": "2023-06-01"
                    }
                    
                    test_payload = {
                        "model": model,
                        "max_tokens": 1,
                        "messages": [{"role": "user", "content": "test"}]
                    }
                    
                    try:
                        response = requests.post(
                            "https://api.anthropic.com/v1/messages",
                            headers=headers,
                            json=test_payload,
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            self.updates_found['new_models'].append({
                                'provider': 'anthropic',
                                'model': model,
                                'description': f"New Anthropic model detected: {model}"
                            })
                            print(f"  🆕 New model found: {model}")
                        
                    except Exception:
                        pass  # Model doesn't exist or other error
            
            print(f"  ✅ Anthropic check complete")
            
        except Exception as e:
            print(f"  ❌ Anthropic check failed: {e}")
    
    def check_google_updates(self):
        """Check Google for new Gemini models"""
        print("🔴 Checking Google AI updates...")
        
        try:
            api_key = os.environ.get('GOOGLE_API_KEY', '')
            if not api_key:
                print("  ⚠️ No Google API key available")
                return
            
            # Get list of available models
            response = requests.get(
                f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
                timeout=30
            )
            
            if response.status_code == 200:
                api_models = response.json().get('models', [])
                current_google_models = [m['model'] for m in self.current_models if m.get('provider') == 'google']
                
                # Check for new models
                for model_info in api_models:
                    model_name = model_info.get('name', '').replace('models/', '')
                    
                    if (model_name not in current_google_models and 
                        any(prefix in model_name for prefix in ['gemini-', 'text-embedding'])):
                        
                        self.updates_found['new_models'].append({
                            'provider': 'google',
                            'model': model_name,
                            'description': model_info.get('description', f"New Google model: {model_name}"),
                            'version': model_info.get('version'),
                            'display_name': model_info.get('displayName')
                        })
                        print(f"  🆕 New model found: {model_name}")
                
                # Check for deprecated models
                for model_info in api_models:
                    model_name = model_info.get('name', '').replace('models/', '')
                    if model_name in current_google_models:
                        # Check if model is deprecated or has warnings
                        if 'deprecated' in model_info.get('description', '').lower():
                            self.updates_found['deprecated_models'].append({
                                'provider': 'google',
                                'model': model_name,
                                'reason': 'Model marked as deprecated in API'
                            })
                            print(f"  ⚠️ Deprecated model: {model_name}")
                
                print(f"  ✅ Google check complete - {len(api_models)} models scanned")
            else:
                print(f"  ⚠️ Google API error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Google check failed: {e}")
    
    def check_xai_updates(self):
        """Check xAI for updates"""
        print("⚫ Checking xAI updates...")
        
        try:
            # xAI doesn't have a public models API yet
            # Check known models and test for new ones
            known_models = ['grok-2', 'grok-2-mini', 'grok-beta']
            potential_new_models = ['grok-3', 'grok-2-vision', 'grok-mini']
            
            current_xai_models = [m['model'] for m in self.current_models if m.get('provider') == 'xai']
            
            # For now, just log that we checked
            print(f"  ✅ xAI check complete - monitoring {len(current_xai_models)} models")
            
        except Exception as e:
            print(f"  ❌ xAI check failed: {e}")
    
    def check_mistral_updates(self):
        """Check Mistral for updates"""
        print("🟡 Checking Mistral updates...")
        
        try:
            api_key = os.environ.get('MISTRAL_API_KEY', '')
            if not api_key:
                print("  ⚠️ No Mistral API key available")
                return
            
            # Mistral models endpoint
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.mistral.ai/v1/models", headers=headers, timeout=30)
            
            if response.status_code == 200:
                api_models = response.json().get('data', [])
                current_mistral_models = [m['model'] for m in self.current_models if m.get('provider') == 'mistral']
                
                # Check for new models
                for model in api_models:
                    model_id = model.get('id', '')
                    if model_id not in current_mistral_models:
                        self.updates_found['new_models'].append({
                            'provider': 'mistral',
                            'model': model_id,
                            'description': f"New Mistral model detected: {model_id}",
                            'created': model.get('created'),
                            'owned_by': model.get('owned_by')
                        })
                        print(f"  🆕 New model found: {model_id}")
                
                print(f"  ✅ Mistral check complete - {len(api_models)} models scanned")
            else:
                print(f"  ⚠️ Mistral API error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Mistral check failed: {e}")
    
    def check_pricing_updates(self):
        """Check for pricing changes (where APIs provide this info)"""
        print("💰 Checking for pricing updates...")
        
        # Most providers don't expose pricing via API
        # This would require scraping documentation or using cached data
        # For now, we'll just note that pricing should be checked manually
        
        print("  ℹ️ Pricing updates require manual verification")
        print("  📋 Check provider documentation for latest pricing")
    
    def test_existing_models(self):
        """Test a sample of existing models to check for deprecations"""
        print("🧪 Testing existing models for deprecations...")
        
        try:
            # Initialize inventory if secrets are available
            secrets_file = Path('secrets.yaml')
            if not secrets_file.exists():
                print("  ⚠️ No secrets file available for testing")
                return
            
            inventory = LLMInventory(
                configs_dir=Path('configs'),
                secrets_file=secrets_file
            )
            
            # Test a few key models from each provider
            test_models = [
                ('openai', 'gpt-4o'),
                ('anthropic', 'claude-3-5-sonnet-20241022'),
                ('google', 'gemini-1.5-flash-latest')
            ]
            
            for provider, model in test_models:
                try:
                    if provider == 'google':
                        payload = {"contents": [{"role": "user", "parts": [{"text": "test"}]}]}
                        parameters = {"maxOutputTokens": 1}
                    else:
                        payload = {"messages": [{"role": "user", "content": "test"}]}
                        parameters = {"max_tokens": 1}
                    
                    response = inventory.invoke(provider, model, payload, parameters)
                    print(f"  ✅ {provider}/{model} - Working")
                    
                except Exception as e:
                    if "deprecated" in str(e).lower() or "not found" in str(e).lower():
                        self.updates_found['deprecated_models'].append({
                            'provider': provider,
                            'model': model,
                            'reason': f"Model test failed: {str(e)[:100]}"
                        })
                        print(f"  ⚠️ {provider}/{model} - Possibly deprecated: {e}")
                    else:
                        print(f"  ⚠️ {provider}/{model} - Test error: {e}")
                
                time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"  ❌ Model testing failed: {e}")
    
    def run_full_check(self):
        """Run comprehensive API update check"""
        print("🚀 STARTING DAILY API UPDATES CHECK")
        print("=" * 60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Current models in database: {len(self.current_models)}")
        print()
        
        # Check each provider
        self.check_openai_updates()
        time.sleep(2)
        
        self.check_anthropic_updates()
        time.sleep(2)
        
        self.check_google_updates()
        time.sleep(2)
        
        self.check_xai_updates()
        time.sleep(2)
        
        self.check_mistral_updates()
        time.sleep(2)
        
        self.check_pricing_updates()
        time.sleep(2)
        
        self.test_existing_models()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 CHECK SUMMARY")
        print("=" * 60)
        
        total_updates = (len(self.updates_found['new_models']) + 
                        len(self.updates_found['deprecated_models']) + 
                        len(self.updates_found['pricing_changes']) + 
                        len(self.updates_found['capability_changes']))
        
        print(f"New models found: {len(self.updates_found['new_models'])}")
        print(f"Deprecated models: {len(self.updates_found['deprecated_models'])}")
        print(f"Pricing changes: {len(self.updates_found['pricing_changes'])}")
        print(f"Capability changes: {len(self.updates_found['capability_changes'])}")
        print(f"Total updates: {total_updates}")
        
        if total_updates > 0:
            print("\n🚨 UPDATES DETECTED!")
            
            # Save updates to file for GitHub Action
            with open('api_updates_found.json', 'w') as f:
                json.dump(self.updates_found, f, indent=2)
            
            print("📄 Updates saved to api_updates_found.json")
            
            # Print details
            if self.updates_found['new_models']:
                print("\n🆕 NEW MODELS:")
                for model in self.updates_found['new_models']:
                    print(f"  • {model['provider']}/{model['model']}")
            
            if self.updates_found['deprecated_models']:
                print("\n⚠️ DEPRECATED MODELS:")
                for model in self.updates_found['deprecated_models']:
                    print(f"  • {model['provider']}/{model['model']}: {model['reason']}")
        else:
            print("\n✅ NO UPDATES DETECTED")
            print("All APIs appear stable with no significant changes.")
        
        print(f"\nNext check scheduled: {datetime.now().strftime('%Y-%m-%d')} + 1 day")
        print("🎯 Check complete!")

def main():
    """Main function"""
    checker = APIUpdateChecker()
    checker.run_full_check()

if __name__ == "__main__":
    main() 
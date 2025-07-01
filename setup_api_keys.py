"""
Interactive script to help set up API keys for testing.
This script will guide you through creating your secrets.yaml file.
"""

import yaml
from pathlib import Path
import getpass


def setup_api_keys():
    """Interactive setup for API keys."""
    print("🔑 LLM Inventory API Key Setup")
    print("=" * 40)
    print("This script will help you set up your API keys for testing.")
    print("You can skip any provider by pressing Enter without typing anything.\n")
    
    secrets = {}
    
    # OpenAI
    print("🔵 OpenAI Setup")
    openai_key = getpass.getpass("Enter your OpenAI API key (starts with 'sk-'): ").strip()
    if openai_key:
        secrets["openai"] = {"api_key": openai_key}
        print("✅ OpenAI key configured")
    else:
        print("⏭️ Skipping OpenAI")
    
    # Anthropic
    print("\n🟠 Anthropic Setup")
    anthropic_key = getpass.getpass("Enter your Anthropic API key (starts with 'sk-ant-'): ").strip()
    if anthropic_key:
        secrets["anthropic"] = {"api_key": anthropic_key}
        print("✅ Anthropic key configured")
    else:
        print("⏭️ Skipping Anthropic")
    
    # Google
    print("\n🔴 Google AI Setup")
    google_key = getpass.getpass("Enter your Google AI API key: ").strip()
    if google_key:
        secrets["google"] = {"api_key": google_key}
        print("✅ Google key configured")
    else:
        print("⏭️ Skipping Google")
    
    # xAI
    print("\n⚫ xAI Setup")
    xai_key = getpass.getpass("Enter your xAI API key: ").strip()
    if xai_key:
        secrets["xai"] = {"api_key": xai_key}
        print("✅ xAI key configured")
    else:
        print("⏭️ Skipping xAI")
    
    # Mistral
    print("\n🟡 Mistral Setup")
    mistral_key = getpass.getpass("Enter your Mistral API key: ").strip()
    if mistral_key:
        secrets["mistral"] = {"api_key": mistral_key}
        print("✅ Mistral key configured")
    else:
        print("⏭️ Skipping Mistral")
    
    # Save to secrets.yaml
    if secrets:
        secrets_file = Path("secrets.yaml")
        
        # Check if secrets.yaml already exists
        if secrets_file.exists():
            overwrite = input(f"\n⚠️ {secrets_file} already exists. Overwrite? (y/N): ").strip().lower()
            if overwrite != 'y':
                print("❌ Setup cancelled")
                return False
        
        # Write the secrets file
        with open(secrets_file, 'w') as f:
            yaml.dump(secrets, f, default_flow_style=False, sort_keys=False)
        
        print(f"\n✅ API keys saved to {secrets_file}")
        print(f"📁 Configured {len(secrets)} provider(s)")
        
        # Show which providers are configured
        print("\n📋 Configured providers:")
        for provider in secrets.keys():
            print(f"  ✅ {provider}")
        
        print(f"\n🚀 You can now run: python test_all_providers.py")
        return True
    else:
        print("\n❌ No API keys provided. Setup cancelled.")
        return False


def check_existing_setup():
    """Check if secrets.yaml already exists and show status."""
    secrets_file = Path("secrets.yaml")
    
    if not secrets_file.exists():
        print("❌ No secrets.yaml file found")
        return False
    
    try:
        with open(secrets_file, 'r') as f:
            secrets = yaml.safe_load(f)
        
        if not secrets:
            print("❌ secrets.yaml is empty")
            return False
        
        print("✅ Found existing secrets.yaml with providers:")
        for provider in secrets.keys():
            print(f"  ✅ {provider}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error reading secrets.yaml: {e}")
        return False


def main():
    """Main function."""
    print("🔍 Checking existing setup...")
    
    if check_existing_setup():
        choice = input("\nExisting setup found. Do you want to:\n1. Keep existing setup\n2. Reconfigure\nChoice (1/2): ").strip()
        
        if choice == "2":
            setup_api_keys()
        else:
            print("✅ Using existing configuration")
            print("🚀 You can run: python test_all_providers.py")
    else:
        print("🆕 Setting up new configuration...")
        setup_api_keys()


if __name__ == "__main__":
    main() 
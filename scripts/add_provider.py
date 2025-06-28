#!/usr/bin/env python3
"""
LLM Provider Addition Script

This script helps you request analysis and integration of new LLM providers.
It can trigger the GitHub Actions workflow or create issues directly.
"""

import os
import sys
import json
import requests
from typing import Optional

def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or user input."""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("GitHub token not found in environment.")
        print("You can:")
        print("1. Set GITHUB_TOKEN environment variable")
        print("2. Enter it now (will not be stored)")
        token = input("Enter GitHub token (or press Enter to skip): ").strip()
    return token if token else None

def trigger_workflow(provider_name: str, api_docs_url: str, repo: str, token: str) -> bool:
    """Trigger the Todo Manager workflow via GitHub API."""
    url = f"https://api.github.com/repos/{repo}/actions/workflows/todo-manager.yml/dispatches"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    data = {
        'ref': 'main',
        'inputs': {
            'provider_name': provider_name,
            'api_docs_url': api_docs_url
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error triggering workflow: {e}")
        return False

def create_issue(provider_name: str, api_docs_url: str, repo: str, token: str) -> bool:
    """Create a GitHub issue for the new provider."""
    url = f"https://api.github.com/repos/{repo}/issues"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    issue_body = f"""## 🎯 New LLM Provider Integration Request

**Provider**: {provider_name}
**API Documentation**: {api_docs_url if api_docs_url else 'To be provided'}

### 📋 Integration Checklist
- [ ] API analysis completed (automated)
- [ ] Dependencies identified
- [ ] Authentication method documented
- [ ] Base adapter implementation
- [ ] Model configuration files
- [ ] Unit tests created
- [ ] Integration tests added
- [ ] Documentation updated
- [ ] Example usage created

### 🔄 Next Steps
1. Wait for automated API analysis
2. Review Claude's assessment
3. Create implementation plan
4. Begin development

### 📊 Estimated Effort
- **Complexity**: TBD (will be assessed by Claude)
- **Timeline**: TBD
- **Dependencies**: TBD

---
*This issue was created by the add_provider.py script*"""

    data = {
        'title': f'Add {provider_name} LLM Provider Support',
        'body': issue_body,
        'labels': ['enhancement', 'provider-integration', 'needs-analysis']
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        issue_data = response.json()
        print(f"✅ Issue created: {issue_data['html_url']}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error creating issue: {e}")
        return False

def main():
    """Main function to handle user input and provider addition."""
    print("🚀 LLM Provider Addition Tool")
    print("=" * 40)
    
    # Get provider information
    provider_name = input("Provider name (e.g., 'Cohere', 'Hugging Face'): ").strip()
    if not provider_name:
        print("❌ Provider name is required!")
        sys.exit(1)
    
    api_docs_url = input("API documentation URL (optional): ").strip()
    
    # Get repository information
    repo = os.getenv('GITHUB_REPOSITORY', 'YCHuang2112sub/LLMInventory')
    print(f"Repository: {repo}")
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("⚠️  No GitHub token provided. Cannot trigger automated analysis.")
        print("You can manually:")
        print(f"1. Go to https://github.com/{repo}/actions/workflows/todo-manager.yml")
        print("2. Click 'Run workflow'")
        print(f"3. Enter provider name: {provider_name}")
        print(f"4. Enter API docs URL: {api_docs_url}")
        return
    
    print(f"\n📋 Summary:")
    print(f"Provider: {provider_name}")
    print(f"API Docs: {api_docs_url or 'Not provided'}")
    print(f"Repository: {repo}")
    
    confirm = input("\nProceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled.")
        return
    
    print("\n🔄 Processing...")
    
    # Try to trigger workflow first (includes Claude analysis)
    if trigger_workflow(provider_name, api_docs_url, repo, token):
        print("✅ Workflow triggered successfully!")
        print("🤖 Claude will analyze the API and create a detailed report.")
        print(f"📊 Check the Actions tab: https://github.com/{repo}/actions")
    else:
        print("⚠️  Workflow trigger failed. Creating issue instead...")
        if create_issue(provider_name, api_docs_url, repo, token):
            print("✅ Issue created successfully!")
        else:
            print("❌ Failed to create issue.")
    
    print(f"\n📈 Monitor progress:")
    print(f"- Issues: https://github.com/{repo}/issues")
    print(f"- TODO List: https://github.com/{repo}/blob/main/TODO.md")
    print(f"- Actions: https://github.com/{repo}/actions")

if __name__ == "__main__":
    main() 
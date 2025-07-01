# 🚀 LLMInventory

[![☕ Buy me a coffee](https://img.shields.io/badge/☕-Buy%20me%20a%20coffee-orange.svg?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/yuchenghuang)

> **Note**: I currently have API keys for OpenAI, Anthropic, and Google providers. If you'd like to help test and support other providers (xAI, Mistral), please consider buying me a coffee to help with API costs! ☕

A comprehensive Python library for managing and accessing multiple Large Language Model (LLM) APIs through a unified interface. Support for **40 models** from **5 major AI providers**.

## ✨ Features

- **40 AI Models** from major providers (OpenAI, Anthropic, Google, xAI, Mistral)
- **Unified API Interface** - Use any model with the same code structure
- **Comprehensive Model Database** with capabilities, pricing, and context windows
- **Type-Safe Configuration** with parameter validation
- **Extensible Architecture** - Easy to add new providers
- **Rich Model Metadata** including capabilities, pricing, and technical specs
- **Embedding Support** - Text embeddings for semantic search
- **Multimodal Capabilities** - Text, vision, audio, and code generation

## 🎯 Supported Providers & Models

### 🟢 OpenAI (6 models) ✅ Tested
- **GPT-4o** - Most advanced multimodal model
- **GPT-4o Mini** - Fast and cost-effective
- **GPT-4 Turbo** - Vision capabilities, 128k context
- **GPT-4.1, GPT-4.1 Mini** - 1M+ context window
- **DALL-E 3** - Image generation

### 🟠 Anthropic (3 models) ✅ Tested
- **Claude 3.5 Sonnet** - Latest with computer use capabilities
- **Claude 3.5 Haiku** - Fast and efficient
- **Claude 3 Haiku** - Cost-effective option

### 🔴 Google (19 models) ✅ Tested
- **Gemini 2.0 Flash** - Latest experimental model
- **Gemini 2.5 Flash** - Enhanced capabilities
- **Gemini 1.5 Flash** - Fast multimodal (multiple variants)
- **Text Embedding 004** - Advanced embeddings
- **Note**: gemini-1.5-pro requires paid tier access

### ⚫ xAI (3 models) ❌ No API Key - Need Support!
- **Grok-2** - Advanced reasoning with real-time data
- **Grok-2 Mini** - Faster version
- **Grok Beta** - Next-generation model

### 🟡 Mistral (9 models) ❌ No API Key - Need Support!
- **Mistral Large** - Most capable model (multiple versions)
- **Codestral** - Code generation specialist
- **Pixtral** - Multimodal with vision
- **Ministral** - Compact edge deployment
- **Mistral Embed** - Text embeddings

## 📊 Current Test Status

**Last Updated**: 2025-06-29 00:21:37

- **Total Models**: 40
- **Working Models**: 26 (65.0% success rate)
- **Providers with API Keys**: 3/5

### Provider Status:
- OpenAI: ✅ Working
- Anthropic: ✅ Working  
- Google: ✅ Working
- xAI: ❌ No API Key
- Mistral: ❌ No API Key

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/LLMInventory.git
cd LLMInventory

# Install dependencies
pip install -r requirements.txt

# Set up your API keys
cp secrets.example.yaml secrets.yaml
# Edit secrets.yaml with your API keys
```

## 🔑 API Keys Setup

Edit `secrets.yaml` with your API keys:

```yaml
openai:
  api_key: "sk-your-openai-key-here"

anthropic:
  api_key: "sk-ant-your-anthropic-key-here"

google:
  api_key: "your-google-ai-api-key-here"

xai:
  api_key: "your-xai-grok-key-here"

mistral:
  api_key: "your-mistral-api-key-here"
```

## 🚀 Quick Start

### Basic Usage

```python
from pathlib import Path
from src.llminventory import LLMInventory

# Initialize the inventory
inventory = LLMInventory(
    configs_dir=Path("configs"),
    secrets_file=Path("secrets.yaml")
)

# List all available models
models = inventory.get_supported_models()
print(f"Available models: {len(models)}")

# Use any model with the same interface
response = inventory.invoke(
    provider="openai",
    model="gpt-4o",
    payload={"messages": [{"role": "user", "content": "Hello!"}]},
    parameters={"temperature": 0.7, "max_tokens": 100}
)

print(response)
```

### Text Generation Examples

```python
# OpenAI GPT-4o
response = inventory.invoke(
    provider="openai",
    model="gpt-4o",
    payload={"messages": [{"role": "user", "content": "Explain quantum computing"}]},
    parameters={"temperature": 0.7, "max_tokens": 200}
)

# Anthropic Claude
response = inventory.invoke(
    provider="anthropic",
    model="claude-3-5-sonnet-20241022",
    payload={"messages": [{"role": "user", "content": "Write a Python function"}]},
    parameters={"temperature": 0.3, "max_tokens": 500}
)

# Google Gemini
response = inventory.invoke(
    provider="google",
    model="gemini-2.0-flash",
    payload={
        "contents": [{
            "role": "user",
            "parts": [{"text": "Analyze this data"}]
        }]
    },
    parameters={"temperature": 0.5, "maxOutputTokens": 300}
)
```

### Embedding Usage

```python
# Google Text Embeddings
embedding_response = inventory.invoke(
    provider="google",
    model="text-embedding-004",
    payload={"input": "Your text to embed here"},
    parameters={"dimensions": 768}
)

# Extract embedding vector
embedding_vector = embedding_response['embedding']['values']
print(f"Embedding dimensions: {len(embedding_vector)}")
```

## 📊 Model Information

Each model includes comprehensive metadata:

- **Capabilities**: text, vision, audio, reasoning, code, embeddings
- **Context Window**: Maximum input tokens
- **Max Output**: Maximum output tokens  
- **Pricing**: Cost per million tokens (where available)
- **Parameters**: Supported configuration options

```python
# Get detailed model information
for model in inventory.get_supported_models():
    print(f"Model: {model['provider']}/{model['model']}")
    print(f"Description: {model['description']}")
    print(f"Capabilities: {model.get('capabilities', [])}")
    print(f"Context Window: {model.get('context_window', 'N/A')}")
    print(f"Pricing: {model.get('pricing', 'N/A')}")
    print("---")
```

## 🏗️ Architecture

```
src/llminventory/
├── __init__.py              # Main LLMInventory class
├── inventory.py             # High-level interface
├── model_config_manager.py  # Configuration management
├── secret_manager.py        # API key management
└── adapters/                # Provider-specific adapters
    ├── base_adapter.py      # Base adapter class
    ├── openai_adapter.py    # OpenAI API adapter
    ├── anthropic_adapter.py # Anthropic API adapter
    ├── google_adapter.py    # Google AI adapter
    ├── xai_adapter.py       # xAI Grok adapter
    └── mistral_adapter.py   # Mistral AI adapter
```

## 🧪 Testing

```bash
# Run comprehensive tests
python comprehensive_model_test.py

# Test specific providers
python test_single_provider.py

# Run unit tests
python -m pytest tests/
```

## 📝 Configuration

Models are configured in `supported_models.yaml`. Each model includes:

```yaml
- provider: openai
  model: gpt-4o
  endpoint: https://api.openai.com/v1/chat/completions
  description: Most advanced GPT-4 model with multimodal capabilities
  capabilities: [text, vision, audio]
  context_window: 128000
  max_output: 16384
  required_fields: [messages]
  parameters:
    temperature:
      type: float
      default: 0.7
      description: Controls randomness in generation
    max_tokens:
      type: integer
      default: 4096
      description: Maximum tokens to generate
  pricing:
    input_cost_per_1m_tokens: 2.5
    output_cost_per_1m_tokens: 10.0
```

## 🔧 Adding New Providers

1. Create a new adapter in `src/llminventory/adapters/`
2. Inherit from `BaseAdapter`
3. Implement the `invoke` method
4. Register in `adapters/__init__.py`
5. Add models to `supported_models.yaml`

## 📋 Requirements

- Python 3.8+
- requests
- PyYAML
- google-generativeai (for Google models)
- anthropic (for Claude models)
- openai (for OpenAI models)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ☕ Support the Project

If you find this project helpful and would like to support development and testing of additional providers, consider buying me a coffee! Your support helps cover API costs for testing new models and providers.

[![Buy me a coffee](https://img.shields.io/badge/☕-Buy%20me%20a%20coffee-orange.svg?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/yuchenghuang)

**Current funding needs:**
- xAI Grok API testing
- Mistral API testing  
- Additional model testing
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- Google for Gemini models
- xAI for Grok models
- Mistral AI for Mistral models

## 📞 Support

If you have questions or need help:

1. Check the [documentation](MODELS.md)
2. Open an [issue](https://github.com/yourusername/LLMInventory/issues)
3. Read the comprehensive test results

---

**Made with ❤️ for the AI community** 

# 🚀 LLMInventory

A comprehensive Python library for managing and accessing multiple Large Language Model (LLM) APIs through a unified interface. Support for 37+ models from 5 major AI providers.

## ✨ Features

- **37+ AI Models** from major providers (OpenAI, Anthropic, Google, xAI, Mistral)
- **Unified API Interface** - Use any model with the same code structure
- **Comprehensive Model Database** with capabilities, pricing, and context windows
- **Type-Safe Configuration** with parameter validation
- **Extensible Architecture** - Easy to add new providers
- **Rich Model Metadata** including capabilities, pricing, and technical specs

## 🎯 Supported Providers & Models

### OpenAI (9 models)
- **GPT-4o** - Most advanced multimodal model
- **GPT-4o Mini** - Fast and cost-effective
- **GPT-4 Turbo** - Vision capabilities, 128k context
- **o1, o1-mini, o3-mini** - Advanced reasoning models
- **GPT-4.1, GPT-4.1 Mini** - 1M+ context window
- **DALL-E 3** - Image generation

### Anthropic (6 models)
- **Claude 4 Opus/Sonnet** - Most capable Claude models
- **Claude 3.7 Sonnet** - Extended thinking capabilities
- **Claude 3.5 Sonnet/Haiku** - Latest with computer use
- **Claude 3 Haiku** - Fast and efficient

### Google (10 models)
- **Gemini 2.0 Flash** - Latest experimental model
- **Gemini 1.5 Pro** - 2M context window
- **Gemini 1.5 Flash** - Fast multimodal
- **Gemma 2 series** - Open source models
- **LearnLM** - Education-focused
- **Text Embedding** - Semantic search

### xAI (3 models)
- **Grok-2** - Advanced reasoning with real-time data
- **Grok-2 Mini** - Faster version
- **Grok Beta** - Next-generation model

### Mistral (9 models)
- **Mistral Large** - Most capable model
- **Codestral** - Code generation specialist
- **Pixtral** - Multimodal with vision
- **Ministral** - Compact edge deployment
- **Mistral Embed** - Text embeddings

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

### Advanced Usage

```python
# Use different providers seamlessly
providers_and_models = [
    ("openai", "gpt-4o"),
    ("anthropic", "claude-3-5-sonnet-20241022"),
    ("google", "gemini-1.5-pro"),
    ("xai", "grok-2"),
    ("mistral", "mistral-large-2411")
]

for provider, model in providers_and_models:
    try:
        response = inventory.invoke(
            provider=provider,
            model=model,
            payload={"messages": [{"role": "user", "content": "Explain AI in one sentence."}]},
            parameters={"temperature": 0.3, "max_tokens": 50}
        )
        print(f"{provider}/{model}: {response}")
    except Exception as e:
        print(f"Error with {provider}/{model}: {e}")
```

## 📊 Model Information

Each model includes comprehensive metadata:

- **Capabilities**: text, vision, audio, reasoning, code, etc.
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
# Run tests
python -m pytest tests/

# Test specific functionality
python -m pytest tests/test_model_config_manager.py
python -m pytest tests/test_secret_manager.py
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

## 🤖 How to Use Claude API Analysis

For adding new LLM providers with automated analysis:

### Method 1: GitHub Actions UI
1. Go to your repo → Actions → "Todo Manager"
2. Click "Run workflow"
3. Enter provider name (e.g., "Cohere")
4. Enter API docs URL
5. Claude will analyze and create detailed report

### Method 2: Python Script
1. Add your Anthropic API key to `secrets.yaml`:
   ```yaml
   anthropic:
     api_key: "sk-ant-your-anthropic-key-here"
   ```
2. Run the provider addition script:
   ```bash
   python scripts/add_provider.py
   ```

### Method 3: Create Issue
Create issue titled "Add [Provider] LLM Provider Support"

## 🔧 Setup Requirements

To enable Claude API analysis, add this secret to your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add `ANTHROPIC_API_KEY` with your Claude API key

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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
3. Read the [development flow](DEVELOPMENT_FLOW.md)

---

**Made with ❤️ for the AI community** 
# Supported Models

This document lists all models supported by the LLMInventory API with detailed specifications.

## OpenAI Models

### GPT-4o
- **Model ID**: `gpt-4o`
- **Description**: Most advanced multimodal model with vision and audio capabilities
- **Context Window**: 128,000 tokens
- **Max Output**: 16,384 tokens
- **Capabilities**: Text, Vision, Audio
- **Pricing**: $2.50 input / $10.00 output (per 1M tokens)

### GPT-4o Mini
- **Model ID**: `gpt-4o-mini`
- **Description**: Faster, more cost-effective version of GPT-4o
- **Context Window**: 128,000 tokens
- **Max Output**: 16,384 tokens
- **Capabilities**: Text, Vision
- **Pricing**: $0.15 input / $0.60 output (per 1M tokens)

### GPT-4 Turbo
- **Model ID**: `gpt-4-turbo`
- **Description**: Latest GPT-4 with vision capabilities and 128k context
- **Context Window**: 128,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: Text, Vision
- **Pricing**: $10.00 input / $30.00 output (per 1M tokens)

### O1 Series
- **Model IDs**: `o1`, `o1-mini`, `o3-mini`
- **Description**: Advanced reasoning models with enhanced problem-solving
- **Context Window**: 200,000 tokens
- **Capabilities**: Advanced reasoning, complex problem solving

## Anthropic Models

### Claude 4 Opus
- **Model ID**: `claude-opus-4-20250514`
- **Description**: Most capable Claude model with extended thinking
- **Context Window**: 200,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: Text, Vision, Extended thinking

### Claude 4 Sonnet
- **Model ID**: `claude-sonnet-4-20250514`
- **Description**: Balanced performance and speed with extended thinking
- **Context Window**: 200,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: Text, Vision, Extended thinking

### Claude 3.7 Sonnet
- **Model ID**: `claude-3-7-sonnet-20241022`
- **Description**: Enhanced Claude with extended thinking capabilities
- **Context Window**: 200,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: Text, Vision, Extended thinking

### Claude 3.5 Sonnet
- **Model ID**: `claude-3-5-sonnet-20241022`
- **Description**: Latest Claude 3.5 with computer use capabilities
- **Context Window**: 200,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: Text, Vision, Computer use

### Claude 3.5 Haiku
- **Model ID**: `claude-3-5-haiku-20241022`
- **Description**: Fast and efficient model with vision support
- **Context Window**: 200,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: Text, Vision

## Google Models

### Gemini 2.0 Flash
- **Model ID**: `gemini-2.0-flash-exp`
- **Description**: Latest experimental Gemini model
- **Context Window**: 1,048,576 tokens
- **Capabilities**: Text, Vision, Audio

### Gemini 1.5 Pro
- **Model ID**: `gemini-1.5-pro-latest`
- **Description**: Most capable Gemini model with 2M context window
- **Context Window**: 2,097,152 tokens
- **Capabilities**: Text, Vision, Audio, Code

### Gemini 1.5 Flash
- **Model ID**: `gemini-1.5-flash-latest`
- **Description**: Fast multimodal model
- **Context Window**: 1,048,576 tokens
- **Capabilities**: Text, Vision, Audio

### Gemma 2 Series
- **Model IDs**: `gemma-2-9b-it`, `gemma-2-27b-it`
- **Description**: Open source models from Google
- **Capabilities**: Text generation, instruction following

## xAI Models

### Grok-2
- **Model ID**: `grok-2`
- **Description**: Advanced reasoning model with real-time data access
- **Context Window**: 131,072 tokens
- **Capabilities**: Text, Real-time data, Advanced reasoning

### Grok-2 Mini
- **Model ID**: `grok-2-mini`
- **Description**: Faster version of Grok-2
- **Context Window**: 131,072 tokens
- **Capabilities**: Text, Real-time data

### Grok Beta
- **Model ID**: `grok-beta`
- **Description**: Next-generation Grok model
- **Context Window**: 131,072 tokens
- **Capabilities**: Text, Advanced reasoning

## Mistral Models

### Mistral Large
- **Model ID**: `mistral-large-2411`
- **Description**: Most capable Mistral model
- **Context Window**: 128,000 tokens
- **Capabilities**: Text, Code, Multilingual

### Codestral
- **Model ID**: `codestral-2405`
- **Description**: Specialized code generation model
- **Context Window**: 32,000 tokens
- **Capabilities**: Code generation, Code completion

### Pixtral
- **Model ID**: `pixtral-12b-2409`
- **Description**: Multimodal model with vision capabilities
- **Context Window**: 128,000 tokens
- **Capabilities**: Text, Vision

### Ministral
- **Model ID**: `ministral-8b-2410`, `ministral-3b-2410`
- **Description**: Compact models for edge deployment
- **Context Window**: 128,000 tokens
- **Capabilities**: Text, Edge deployment

### Mistral Embed
- **Model ID**: `mistral-embed`
- **Description**: Text embedding model
- **Capabilities**: Text embeddings, Semantic search

## Parameter Guidelines

### Temperature
- **0.0 - 0.3**: Deterministic, analytical tasks
- **0.3 - 0.7**: Balanced responses (recommended default: 0.7)
- **0.7 - 1.0**: Creative, varied outputs

### Max Tokens
- **Short responses**: 100-500 tokens
- **Medium responses**: 500-2000 tokens
- **Long responses**: 2000+ tokens

### Top-p
- **Default**: Let API use provider defaults
- **Custom**: 0.9-0.99 for most use cases

## Usage Notes

### Authentication
All models require appropriate API keys configured in `secrets.yaml`.

### Rate Limits
Each provider has different rate limits. Monitor usage to avoid hitting limits.

### Cost Optimization
- Use smaller models for simple tasks
- Implement caching for repeated requests
- Monitor token usage

### Error Handling
- Always implement proper error handling
- Check for rate limit errors
- Validate responses before processing 
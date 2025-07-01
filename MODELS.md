# Supported Models

This document lists all models supported by the LLMInventory API with detailed specifications and test results.

**Last Updated**: 2025-06-29 00:21:37
**Total Models**: 40
**Test Results**: Based on comprehensive testing with available API keys

## Test Status Overview

- **OPENAI**: ✅ 5/6 models working (83.3%)
- **ANTHROPIC**: ✅ 3/3 models working (100.0%)
- **GOOGLE**: ✅ 18/19 models working (94.7%)
- **XAI**: ❌ 0/3 models working (0.0%)
- **MISTRAL**: ❌ 0/9 models working (0.0%)

## 🟢 OPENAI Models

**Status**: ✅ API Key Available - 5/6 models working

### gpt-4o
- **Model ID**: `gpt-4o`
- **Description**: Most advanced GPT-4 model with multimodal capabilities
- **Test Status**: ✅ Working (1.15s)
- **Context Window**: 128,000 tokens
- **Max Output**: 16,384 tokens
- **Capabilities**: text, vision, audio
- **Pricing**: $2.5 input / $10.0 output (per 1M tokens)

### gpt-4o-mini
- **Model ID**: `gpt-4o-mini`
- **Description**: Smaller, faster, cheaper GPT-4o model
- **Test Status**: ✅ Working (1.95s)
- **Context Window**: 128,000 tokens
- **Max Output**: 16,384 tokens
- **Capabilities**: text, vision
- **Pricing**: $0.15 input / $0.6 output (per 1M tokens)

### gpt-4-turbo
- **Model ID**: `gpt-4-turbo`
- **Description**: The latest GPT-4 Turbo model with vision capabilities. Vision requests have a separate rate limit. For both vision and text requests, the model supports a 128k context window.
- **Test Status**: ✅ Working (1.35s)
- **Context Window**: 128,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, vision
- **Pricing**: $10.0 input / $30.0 output (per 1M tokens)

### gpt-4.1
- **Model ID**: `gpt-4.1`
- **Description**: GPT-4.1 with 1M+ context window
- **Test Status**: ✅ Working (0.79s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 32,768 tokens
- **Capabilities**: text

### gpt-4.1-mini
- **Model ID**: `gpt-4.1-mini`
- **Description**: Smaller GPT-4.1 model with large context
- **Test Status**: ✅ Working (1.25s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 32,768 tokens
- **Capabilities**: text

### dall-e-3
- **Model ID**: `dall-e-3`
- **Description**: Advanced image generation model
- **Test Status**: ❌ Failed: Missing required field in payload: 'prompt'
- **Context Window**: N/A
- **Max Output**: N/A
- **Capabilities**: image_generation

## 🟠 ANTHROPIC Models

**Status**: ✅ API Key Available - 3/3 models working

### claude-3-5-sonnet-20241022
- **Model ID**: `claude-3-5-sonnet-20241022`
- **Description**: Latest Claude 3.5 Sonnet with computer use capabilities
- **Test Status**: ✅ Working (2.77s)
- **Context Window**: 200,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, computer_use

### claude-3-5-haiku-20241022
- **Model ID**: `claude-3-5-haiku-20241022`
- **Description**: Fast and efficient Claude 3.5 Haiku
- **Test Status**: ✅ Working (1.68s)
- **Context Window**: 200,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision

### claude-3-haiku-20240307
- **Model ID**: `claude-3-haiku-20240307`
- **Description**: Anthropic's fastest model, designed for near-instant responsiveness and high throughput. Supports vision inputs.
- **Test Status**: ✅ Working (0.93s)
- **Context Window**: 200,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, vision

## 🔴 GOOGLE Models

**Status**: ✅ API Key Available - 18/19 models working

### gemini-2.0-flash-exp
- **Model ID**: `gemini-2.0-flash-exp`
- **Description**: Latest experimental Gemini 2.0 Flash model
- **Test Status**: ✅ Working (9.54s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-1.5-pro
- **Model ID**: `gemini-1.5-pro`
- **Description**: Most capable Gemini model with 2M context
- **Test Status**: ❌ Failed: Google API request failed: 429 Client Error: Too Many Requests for url: https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=AIzaSyBH6tES8pjryqXPG-JZLm8eM-ue29P3XsE
- **Context Window**: 2,000,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, code

### gemini-1.5-flash
- **Model ID**: `gemini-1.5-flash`
- **Description**: Fast and efficient Gemini model
- **Test Status**: ✅ Working (0.96s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio

### gemini-1.5-flash-8b
- **Model ID**: `gemini-1.5-flash-8b`
- **Description**: Smaller, faster Gemini Flash model
- **Test Status**: ✅ Working (0.94s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision

### gemini-1.5-flash-latest
- **Model ID**: `gemini-1.5-flash-latest`
- **Description**: Latest stable Gemini 1.5 Flash model
- **Test Status**: ✅ Working (0.84s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio

### gemini-1.5-flash-002
- **Model ID**: `gemini-1.5-flash-002`
- **Description**: Gemini 1.5 Flash version 002
- **Test Status**: ✅ Working (0.73s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio

### gemini-1.5-flash-8b-001
- **Model ID**: `gemini-1.5-flash-8b-001`
- **Description**: Gemini 1.5 Flash 8B version 001
- **Test Status**: ✅ Working (0.81s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision

### gemini-1.5-flash-8b-latest
- **Model ID**: `gemini-1.5-flash-8b-latest`
- **Description**: Latest Gemini 1.5 Flash 8B model
- **Test Status**: ✅ Working (0.68s)
- **Context Window**: 1,000,000 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision

### gemini-2.5-flash
- **Model ID**: `gemini-2.5-flash`
- **Description**: Latest Gemini 2.5 Flash model with enhanced capabilities
- **Test Status**: ✅ Working (6.27s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 65,536 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-2.5-flash-preview-05-20
- **Model ID**: `gemini-2.5-flash-preview-05-20`
- **Description**: Preview version of Gemini 2.5 Flash
- **Test Status**: ✅ Working (1.04s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 65,536 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-2.5-flash-lite-preview-06-17
- **Model ID**: `gemini-2.5-flash-lite-preview-06-17`
- **Description**: Lightweight version of Gemini 2.5 Flash for high throughput
- **Test Status**: ✅ Working (0.64s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 65,536 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-2.0-flash
- **Model ID**: `gemini-2.0-flash`
- **Description**: Stable Gemini 2.0 Flash model
- **Test Status**: ✅ Working (1.05s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-2.0-flash-001
- **Model ID**: `gemini-2.0-flash-001`
- **Description**: Gemini 2.0 Flash version 001
- **Test Status**: ✅ Working (1.06s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-2.0-flash-exp-image-generation
- **Model ID**: `gemini-2.0-flash-exp-image-generation`
- **Description**: Experimental Gemini 2.0 Flash with image generation capabilities
- **Test Status**: ✅ Working (0.83s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, image_generation, multimodal

### gemini-2.0-flash-lite
- **Model ID**: `gemini-2.0-flash-lite`
- **Description**: Lightweight Gemini 2.0 Flash for cost efficiency
- **Test Status**: ✅ Working (1.25s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-2.0-flash-lite-001
- **Model ID**: `gemini-2.0-flash-lite-001`
- **Description**: Gemini 2.0 Flash Lite version 001
- **Test Status**: ✅ Working (0.74s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-2.0-flash-lite-preview-02-05
- **Model ID**: `gemini-2.0-flash-lite-preview-02-05`
- **Description**: Preview version of Gemini 2.0 Flash Lite
- **Test Status**: ✅ Working (0.73s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, multimodal

### gemini-2.0-flash-lite-preview
- **Model ID**: `gemini-2.0-flash-lite-preview`
- **Description**: Latest preview of Gemini 2.0 Flash Lite
- **Test Status**: ✅ Working (0.84s)
- **Context Window**: 1,048,576 tokens
- **Max Output**: 8,192 tokens
- **Capabilities**: text, vision, audio, multimodal

### text-embedding-004
- **Model ID**: `text-embedding-004`
- **Description**: Latest text embedding model
- **Test Status**: ✅ Working (0.72s)
- **Context Window**: 2,048 tokens
- **Max Output**: N/A
- **Capabilities**: embeddings

## ⚫ XAI Models

**Status**: ❌ No API Key - Cannot test models

### grok-2
- **Model ID**: `grok-2`
- **Description**: Advanced Grok model with reasoning capabilities
- **Test Status**: ❌ Failed: "API key for provider 'xai' not found in secrets."
- **Context Window**: 131,072 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, reasoning, real_time_data

### grok-2-mini
- **Model ID**: `grok-2-mini`
- **Description**: Smaller, faster version of Grok-2
- **Test Status**: ❌ Failed: "API key for provider 'xai' not found in secrets."
- **Context Window**: 131,072 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, reasoning

### grok-beta
- **Model ID**: `grok-beta`
- **Description**: Beta version of next-generation Grok
- **Test Status**: ❌ Failed: "API key for provider 'xai' not found in secrets."
- **Context Window**: 131,072 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, reasoning, real_time_data

## 🟡 MISTRAL Models

**Status**: ❌ No API Key - Cannot test models

### mistral-large-2411
- **Model ID**: `mistral-large-2411`
- **Description**: Latest and most capable Mistral model
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 128,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, code, reasoning, function_calling

### mistral-large-2407
- **Model ID**: `mistral-large-2407`
- **Description**: Previous version of Mistral Large
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 128,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, code, reasoning, function_calling

### mistral-small-2409
- **Model ID**: `mistral-small-2409`
- **Description**: Efficient model for everyday tasks
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 128,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, code

### codestral-2405
- **Model ID**: `codestral-2405`
- **Description**: Specialized model for code generation and completion
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 32,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: code, text

### codestral-mamba-2407
- **Model ID**: `codestral-mamba-2407`
- **Description**: Mamba-based code model with linear scaling
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 256,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: code, text

### pixtral-12b-2409
- **Model ID**: `pixtral-12b-2409`
- **Description**: Multimodal model with vision capabilities
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 128,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, vision, multimodal

### ministral-8b-2410
- **Model ID**: `ministral-8b-2410`
- **Description**: Compact model for edge deployment
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 128,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text, code

### ministral-3b-2410
- **Model ID**: `ministral-3b-2410`
- **Description**: Ultra-compact model for lightweight tasks
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 128,000 tokens
- **Max Output**: 4,096 tokens
- **Capabilities**: text

### mistral-embed
- **Model ID**: `mistral-embed`
- **Description**: Text embedding model for semantic search
- **Test Status**: ❌ Failed: "API key for provider 'mistral' not found in secrets."
- **Context Window**: 8,192 tokens
- **Max Output**: N/A
- **Capabilities**: embeddings

## Usage Guidelines

### Parameter Recommendations

#### Temperature
- **0.0 - 0.3**: Deterministic, analytical tasks
- **0.3 - 0.7**: Balanced responses (recommended default: 0.7)
- **0.7 - 1.0**: Creative, varied outputs

#### Max Tokens
- **Short responses**: 100-500 tokens
- **Medium responses**: 500-2000 tokens
- **Long responses**: 2000+ tokens

#### Provider-Specific Notes

##### OpenAI
- Use `messages` format for chat models
- DALL-E 3 requires `prompt` field instead of `messages`
- GPT-4.1 models have 1M+ context windows

##### Anthropic  
- All models support vision capabilities
- Use `messages` format
- Claude 3.5 models have computer use capabilities

##### Google
- Use `contents` format with `parts` structure
- Embedding models use `input` field
- Some models require paid tier access (gemini-1.5-pro)
- Excellent multimodal capabilities

##### xAI
- Grok models have real-time data access
- Use standard `messages` format
- Advanced reasoning capabilities

##### Mistral
- Codestral specialized for code generation
- Pixtral supports vision
- Ministral models optimized for edge deployment

### Authentication Requirements

All models require appropriate API keys configured in `secrets.yaml`:

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

### Rate Limits & Cost Optimization

- Each provider has different rate limits
- Monitor usage to avoid hitting limits
- Use smaller models for simple tasks
- Implement caching for repeated requests
- Consider context window limits for long conversations

### Error Handling Best Practices

- Always implement proper error handling
- Check for rate limit errors (429)
- Validate responses before processing
- Handle model-not-found errors gracefully
- Implement retry logic with exponential backoff

## Testing Information

This documentation is based on comprehensive testing performed on {datetime.now().strftime("%Y-%m-%d")}. 

**Test Coverage**:
- All models with available API keys tested
- Response time measurements included
- Error conditions documented
- Capability verification performed

For the most up-to-date test results, run:
```bash
python comprehensive_model_test.py
```

# Custom Vision Model UI Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Multi-Vision Toolkit                                       │
│                                                              │
│  Model: [florence2 ▼]  →  Model: [custom-api ▼]  🌙 Theme │
│         [qwen-captioner]           ^                         │
│         [qwen3         ]           │                         │
│         [custom-api    ] ──────────┘                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘

When "custom-api" is selected for the first time:

┌──────────────────────────────────────────────────────────────┐
│  Configure Custom Vision Model                         [×]   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Model Name:                                                 │
│  [Custom Model_________________________________]             │
│  Display name for this model                                │
│                                                              │
│  API URL:                                                    │
│  [https://api.example.com/v1/chat/completions]             │
│  Full endpoint URL                                          │
│                                                              │
│  API Key:                                                    │
│  [****************************************]                  │
│  ☐ Show API Key                                             │
│                                                              │
│  API Format:                                                 │
│  [openai        ▼]                                          │
│  openai: OpenAI/compatible | anthropic: Claude | generic   │
│                                                              │
│  Model ID (optional):                                        │
│  [gpt-4-vision-preview_____________________]                │
│  Specific model identifier to use                           │
│                                                              │
│                                                              │
│  [Test Connection]  ✓ Connection successful                 │
│                                                              │
│                                          [Cancel]  [Save]   │
└──────────────────────────────────────────────────────────────┘

After saving, the custom model is ready to use:

┌─────────────────────────────────────────────────────────────┐
│  Multi-Vision Toolkit                                       │
│                                                              │
│  Model: [custom-api ▼]  🌙 Theme                           │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                       │   │
│  │         [Image Display Area]                         │   │
│  │                                                       │   │
│  │         Using Custom Model API                       │   │
│  │                                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  Image Analysis                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Generated caption using custom vision model...       │   │
│  │                                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  [Approve] [Reject] [Re-caption]                            │
│                                                              │
│  Status: custom-api model ready                             │
└─────────────────────────────────────────────────────────────┘
```

## Supported API Formats

### 1. OpenAI Format
- OpenAI GPT-4 Vision
- Azure OpenAI
- Compatible APIs (LiteLLM, Ollama, etc.)

### 2. Anthropic Format
- Anthropic Claude 3 (Opus, Sonnet, Haiku)
- Claude with Vision capabilities

### 3. Generic Format
- Custom self-hosted models
- Any API with simple JSON request/response
- Flexible response parsing

## Key Features

✓ Secure API key handling (masked input)
✓ Connection testing before use
✓ Multiple API format support
✓ Integrated with existing template system
✓ Same workflow as built-in models
✓ Automatic image preprocessing (resize, base64 encoding)

## Example Use Cases

1. **Use GPT-4 Vision** for high-quality captions
2. **Use Claude 3** for detailed image analysis
3. **Use custom models** for specialized domains
4. **Switch between models** for comparison
5. **Batch process** with API models

# Custom Vision Model Integration Guide

This guide explains how to use custom vision models with the Multi-Vision Toolkit by providing an API URL and API key.

## Overview

The Multi-Vision Toolkit now supports custom vision models through API integration. This allows you to use any vision API that accepts images and returns text descriptions, including:

- OpenAI's GPT-4 Vision
- Anthropic's Claude with Vision
- Google's Gemini Vision
- Custom/self-hosted vision models
- Any other vision API that follows standard formats

## Features

- **Multiple API Format Support**: Compatible with OpenAI, Anthropic, and generic API formats
- **Secure Configuration**: API keys are stored securely during runtime
- **Connection Testing**: Test your API connection before using the model
- **Template System Integration**: Works with the existing template system for consistent prompting
- **Easy Model Switching**: Switch between custom and built-in models seamlessly

## Quick Start

### Step 1: Select Custom API Model

1. Launch the Multi-Vision Toolkit
2. In the top-right corner, find the **Model** dropdown
3. Select **custom-api** from the dropdown

### Step 2: Configure Your Custom Model

When you select custom-api for the first time, a configuration dialog will appear:

1. **Model Name**: Enter a display name for your model (e.g., "GPT-4 Vision", "Claude 3")
2. **API URL**: Enter the full endpoint URL
   - OpenAI: `https://api.openai.com/v1/chat/completions`
   - Anthropic: `https://api.anthropic.com/v1/messages`
   - Custom: Your API endpoint URL
3. **API Key**: Enter your API authentication key
   - Use "Show API Key" checkbox to verify your key
4. **API Format**: Select the appropriate format:
   - `openai`: For OpenAI and compatible APIs
   - `anthropic`: For Anthropic Claude API
   - `generic`: For custom/generic APIs
5. **Model ID (optional)**: Specify a model identifier (e.g., "gpt-4-vision-preview")

### Step 3: Test Connection

Click the **Test Connection** button to verify your API configuration before saving.

### Step 4: Start Using

Click **Save** to activate your custom model. You can now use it just like the built-in models!

## API Format Details

### OpenAI Format

Works with OpenAI's Vision API and compatible endpoints.

**Expected Request Format:**
```json
{
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Describe this image"},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
      ]
    }
  ],
  "max_tokens": 1000
}
```

**Expected Response Format:**
```json
{
  "choices": [
    {
      "message": {
        "content": "Description text here..."
      }
    }
  ]
}
```

### Anthropic Format

Works with Anthropic's Claude Vision API.

**Expected Request Format:**
```json
{
  "model": "claude-3-opus-20240229",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": "..."
          }
        },
        {"type": "text", "text": "Describe this image"}
      ]
    }
  ]
}
```

**Expected Response Format:**
```json
{
  "content": [
    {
      "text": "Description text here..."
    }
  ]
}
```

### Generic Format

Simple format for custom APIs.

**Expected Request Format:**
```json
{
  "image": "base64_encoded_image_data",
  "prompt": "Describe this image",
  "max_tokens": 1000
}
```

**Expected Response Format** (flexible, tries these fields):
```json
{
  "text": "Description text here..."
}
// OR
{
  "response": "Description text here..."
}
// OR
{
  "description": "Description text here..."
}
// OR
{
  "caption": "Description text here..."
}
```

## Example Configurations

### OpenAI GPT-4 Vision

```
Model Name: GPT-4 Vision
API URL: https://api.openai.com/v1/chat/completions
API Key: sk-your-openai-api-key
API Format: openai
Model ID: gpt-4-vision-preview
```

### Anthropic Claude 3

```
Model Name: Claude 3 Opus
API URL: https://api.anthropic.com/v1/messages
API Key: sk-ant-your-anthropic-key
API Format: anthropic
Model ID: claude-3-opus-20240229
```

### Custom Self-Hosted Model

```
Model Name: My Custom Model
API URL: https://your-server.com/api/vision
API Key: your-custom-api-key
API Format: generic
Model ID: (leave empty)
```

## Image Processing

The custom model automatically handles:

- **Format Conversion**: Images are converted to RGB JPEG
- **Size Optimization**: Images larger than 2048px are automatically resized
- **Base64 Encoding**: Images are encoded to base64 for API transmission
- **Quality Preservation**: Uses 95% JPEG quality for optimal results

## Troubleshooting

### Connection Test Fails

1. **Check URL**: Ensure the URL is correct and includes `https://`
2. **Verify API Key**: Double-check your API key for typos
3. **Test Independently**: Try your API with curl or Postman
4. **Check Network**: Ensure you have internet connectivity
5. **Review Logs**: Check `app.log` for detailed error messages

### Model Initialization Fails

1. **Install Dependencies**: Ensure `requests` library is installed
   ```bash
   pip install requests
   ```
2. **Check API Format**: Verify you selected the correct API format
3. **Review API Documentation**: Ensure your API matches the expected format
4. **Check API Limits**: Verify you haven't exceeded rate limits

### Unexpected Results

1. **Check Prompts**: Review the templates in use (standard/detailed/creative)
2. **Test API Directly**: Verify the API works correctly outside the toolkit
3. **Review Model ID**: Ensure the Model ID matches your API's requirements
4. **Check Logs**: Look for parsing errors in `app.log`

## Advanced Usage

### Custom Templates

You can create custom prompt templates for your API model:

1. Access the template system (if available in UI)
2. Create templates for the "custom" model
3. Use template variables like `{trigger_word}`, `{quality_mode}`, etc.

### API Authentication

The toolkit supports two authentication methods:

- **Bearer Token** (OpenAI, Generic): `Authorization: Bearer {api_key}`
- **API Key Header** (Anthropic): `x-api-key: {api_key}`

Both are automatically configured based on the API format you select.

### Rate Limiting

The custom model respects standard HTTP rate limiting. If you encounter rate limit errors:

1. Add delays between batch processing operations
2. Use a higher tier API plan
3. Implement retry logic in your workflow

## Security Notes

- API keys are stored in memory only during runtime
- Keys are not persisted to disk automatically
- Use environment variables for additional security if needed
- Never commit API keys to version control

## Requirements

- Python 3.11+
- `requests>=2.31.0` (automatically installed from requirements.txt)
- Valid API endpoint with vision capabilities
- API key with appropriate permissions

## Support

For issues or questions:
1. Check `app.log` for error details
2. Review this documentation
3. Test your API independently
4. Open an issue on GitHub with log excerpts

## Future Enhancements

Planned features for custom models:
- [ ] Persistent configuration storage
- [ ] Multiple custom model profiles
- [ ] Response caching
- [ ] Batch API optimization
- [ ] Custom header support
- [ ] Retry logic with exponential backoff

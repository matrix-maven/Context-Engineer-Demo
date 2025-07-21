# Configuration Guide

This document provides comprehensive guidance on configuring the Context Engineering Demo application for different environments.

## Overview

The application uses a layered configuration approach:

1. **Environment Variables** - Primary configuration method
2. **Environment Files** - `.env`, `.env.development`, `.env.production`
3. **Pydantic Settings** - Type-safe configuration validation
4. **Default Values** - Sensible defaults for all settings

## Quick Start

### 1. Basic Setup

```bash
# Copy the template to create your configuration
cp .env.template .env

# Edit the file and add your API keys
nano .env  # or your preferred editor

# Validate your configuration
python validate_config.py

# Start the application
streamlit run main.py
```

### 2. Get API Keys

You'll need at least one AI provider API key:

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **OpenRouter**: https://openrouter.ai/keys

## Configuration Files

### Environment Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `.env.template` | Template with all options | Copy to create `.env` |
| `.env` | Your local configuration | Local development (not committed) |
| `.env.development` | Development defaults | Development environment |
| `.env.production` | Production template | Production deployment |

### Configuration Modules

| Module | Purpose |
|--------|---------|
| `config/settings.py` | Application settings with Pydantic validation |
| `config/ai_config.py` | AI provider configurations |
| `config/validation.py` | Configuration validation and startup checks |

## Configuration Options

### AI Provider Settings

#### OpenAI Configuration

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
OPENAI_MODEL=gpt-3.5-turbo          # Default model
OPENAI_BASE_URL=https://api.openai.com/v1  # Custom endpoint
```

**Recommended Models:**
- Development: `gpt-3.5-turbo` (fast, cost-effective)
- Production: `gpt-4-turbo-preview` (higher quality)

#### Anthropic Configuration

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional
ANTHROPIC_MODEL=claude-3-haiku-20240307     # Default model
ANTHROPIC_BASE_URL=https://api.anthropic.com  # Custom endpoint
```

**Recommended Models:**
- Development: `claude-3-haiku-20240307` (fast, cost-effective)
- Production: `claude-3-sonnet-20240229` (balanced performance)

#### Google Gemini Configuration

```bash
# Required
GEMINI_API_KEY=AIzaSy-your-key-here

# Optional
GEMINI_MODEL=gemini-1.5-flash       # Default model
GEMINI_BASE_URL=https://generativelanguage.googleapis.com  # Custom endpoint
```

#### OpenRouter Configuration

```bash
# Required
OPENROUTER_API_KEY=sk-or-your-key-here

# Optional
OPENROUTER_MODEL=openai/gpt-3.5-turbo      # Default model
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1  # Custom endpoint
```

### Application Settings

#### Core Settings

```bash
# Default AI provider (openai, anthropic, gemini, openrouter)
AI_PROVIDER=openai

# Application title and branding
APP_TITLE=Context Engineering Demo

# Enable debug mode (true/false)
DEBUG=false

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

#### AI Model Parameters

```bash
# Response creativity (0.0 = deterministic, 2.0 = very creative)
AI_TEMPERATURE=0.7

# Maximum response length in tokens
AI_MAX_TOKENS=500

# Request timeout in seconds
AI_TIMEOUT=30
```

#### Performance Settings

```bash
# Enable response caching (true/false)
ENABLE_CACHING=true

# Cache time-to-live in seconds
CACHE_TTL=3600

# Maximum context data size
MAX_CONTEXT_SIZE=10000

# Context refresh interval in seconds
CONTEXT_REFRESH_INTERVAL=300
```

## Environment-Specific Configurations

### Development Environment

**Characteristics:**
- Faster, cheaper AI models
- Verbose logging
- Disabled caching for fresh responses
- Debug features enabled

**Setup:**
```bash
# Use development defaults
cp .env.development .env

# Add your API keys
echo "OPENAI_API_KEY=your-key-here" >> .env
echo "GEMINI_API_KEY=your-key-here" >> .env

# Validate configuration
python validate_config.py --verbose
```

**Key Settings:**
```bash
DEBUG=true
LOG_LEVEL=DEBUG
ENABLE_CACHING=false
AI_TEMPERATURE=0.8
AI_MAX_TOKENS=300
```

### Production Environment

**Characteristics:**
- High-quality AI models
- Optimized performance
- Security hardening
- Monitoring enabled

**Setup:**
```bash
# Use environment variables instead of .env files
export OPENAI_API_KEY="your-production-key"
export AI_PROVIDER="openai"
export LOG_LEVEL="INFO"
export ENABLE_CACHING="true"

# Validate before deployment
python validate_config.py --quiet
```

**Key Settings:**
```bash
DEBUG=false
LOG_LEVEL=INFO
ENABLE_CACHING=true
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500
```

## Configuration Validation

### Automatic Validation

The application automatically validates configuration on startup:

```python
from config.validation import validate_and_setup

# This runs automatically when the app starts
success, result = validate_and_setup()
if not success:
    # Handle configuration errors
    pass
```

### Manual Validation

Run validation checks manually:

```bash
# Basic validation
python validate_config.py

# Detailed output
python validate_config.py --verbose

# Fix common issues automatically
python validate_config.py --fix

# Quiet mode (errors/warnings only)
python validate_config.py --quiet
```

### Validation Checks

The validator checks:

- ✅ At least one AI provider is configured
- ✅ API keys are present and valid format
- ✅ Numeric settings are within valid ranges
- ✅ Required directories exist
- ✅ Dependencies are installed
- ✅ Settings pass Pydantic validation

## Troubleshooting

### Common Issues

#### No AI Providers Configured

**Error:** `No AI provider API keys configured`

**Solution:**
```bash
# Add at least one API key to .env
echo "OPENAI_API_KEY=your-key-here" >> .env
```

#### Invalid API Key Format

**Error:** `Invalid API key for openai`

**Solution:**
- Check that your API key is correct
- Ensure no extra spaces or characters
- Verify the key hasn't expired

#### Configuration File Not Found

**Error:** `No .env file found`

**Solution:**
```bash
# Create from template
cp .env.template .env

# Or use the fix command
python validate_config.py --fix
```

#### Import Errors

**Error:** `ModuleNotFoundError: No module named 'openai'`

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt
```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG

# Or as environment variable
export DEBUG=true
export LOG_LEVEL=DEBUG
```

Debug mode provides:
- Detailed error messages
- Configuration status in UI
- Performance metrics
- Request/response logging

### Configuration Status

Check configuration status programmatically:

```python
from config.validation import get_configuration_status

status = get_configuration_status()
print(f"Valid: {status['is_valid']}")
print(f"Providers: {status['available_providers']}")
```

## Security Best Practices

### API Key Management

1. **Never commit API keys to version control**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   echo ".env.local" >> .gitignore
   ```

2. **Use different keys for different environments**
   - Development: Limited quota keys
   - Production: Full access keys with monitoring

3. **Rotate keys regularly**
   - Set up key rotation schedule
   - Monitor for unusual usage patterns

4. **Use environment variables in production**
   ```bash
   # Instead of .env files
   export OPENAI_API_KEY="$PRODUCTION_OPENAI_KEY"
   ```

### Production Security

1. **Disable debug mode**
   ```bash
   DEBUG=false
   ```

2. **Use appropriate log levels**
   ```bash
   LOG_LEVEL=INFO  # or WARNING for production
   ```

3. **Enable security headers**
   ```bash
   SECURE_HEADERS=true
   ```

4. **Set up monitoring**
   ```bash
   ENABLE_METRICS=true
   METRICS_ENDPOINT=/metrics
   ```

## Advanced Configuration

### Custom AI Providers

To add a new AI provider:

1. Create provider class in `services/`
2. Add to `AIProvider` enum in `config/settings.py`
3. Add configuration mapping in `config/ai_config.py`
4. Update validation logic

### Environment-Specific Overrides

Use multiple environment files:

```bash
# Load base configuration
python-dotenv .env

# Override with environment-specific settings
python-dotenv .env.production
```

### Configuration Profiles

Create configuration profiles for different use cases:

```bash
# profiles/.env.demo
AI_TEMPERATURE=1.0
AI_MAX_TOKENS=200
ENABLE_CACHING=false

# profiles/.env.testing
AI_PROVIDER=mock
MOCK_AI_RESPONSES=true
```

## Migration Guide

### From v1.0 to v2.0

If upgrading from an older version:

1. **Update environment variables**
   ```bash
   # Old format
   OPENAI_KEY=...
   
   # New format
   OPENAI_API_KEY=...
   ```

2. **Run configuration migration**
   ```bash
   python validate_config.py --fix
   ```

3. **Update dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## Support

For configuration issues:

1. Run the validator: `python validate_config.py --verbose`
2. Check the logs in `logs/app.log`
3. Review this documentation
4. Check the GitHub issues for known problems

---

*Last updated: 2025-01-16*
*Configuration version: 2.0.0*
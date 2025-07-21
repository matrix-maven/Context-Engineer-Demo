# Dependencies and Installation Guide

This document provides detailed information about the Context Engineering Demo's dependencies, installation requirements, and troubleshooting.

## 📦 Dependency Overview

The `requirements.txt` file has been organized into logical sections for better maintainability and understanding:

### Core Application Framework
- **streamlit>=1.28.0**: Web application framework for the demo interface
- **pandas>=2.0.0**: Data manipulation and analysis library
- **numpy>=1.24.0**: Numerical computing library
- **faker>=19.0.0**: Realistic data generation for context services

### AI Provider Dependencies
- **openai>=1.0.0**: OpenAI API client for GPT models
- **anthropic>=0.7.0**: Anthropic API client for Claude models
- **google-generativeai>=0.3.0**: Google Gemini API client
- **requests>=2.31.0**: HTTP library for OpenRouter and other API calls

### Configuration and Environment Management
- **python-dotenv>=1.0.0**: Environment variable loading from .env files
- **pydantic>=2.0.0**: Data validation and settings management
- **pydantic-settings>=2.0.0**: Settings management with Pydantic

### Error Handling and Logging
- **structlog>=23.0.0**: Structured logging for better debugging and monitoring

### Testing Dependencies
- **pytest>=7.0.0**: Core testing framework
- **pytest-mock>=3.10.0**: Mocking utilities for tests
- **pytest-asyncio>=0.21.0**: Async testing support for AI provider calls
- **pytest-cov>=4.0.0**: Code coverage reporting
- **responses>=0.23.0**: HTTP mocking for AI provider testing

### Development Dependencies (Optional)
The following dependencies are commented out by default but can be uncommented for development:
- **black>=23.0.0**: Code formatting
- **flake8>=6.0.0**: Code linting
- **mypy>=1.0.0**: Static type checking

## 🚀 Installation Methods

### Method 1: Standard Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd context-engineering-demo

# Install all dependencies
pip install -r requirements.txt
```

### Method 2: Minimal Installation (Static Demo Only)

If you only want to run the static demo without AI providers:

```bash
# Install core dependencies only
pip install streamlit>=1.28.0 pandas>=2.0.0 numpy>=1.24.0 faker>=19.0.0 python-dotenv>=1.0.0 pydantic>=2.0.0 pydantic-settings>=2.0.0 structlog>=23.0.0
```

### Method 3: Development Installation

For development with all tools:

```bash
# Install all dependencies including development tools
pip install -r requirements.txt

# Uncomment development dependencies in requirements.txt first:
# black>=23.0.0
# flake8>=6.0.0  
# mypy>=1.0.0

pip install black>=23.0.0 flake8>=6.0.0 mypy>=1.0.0
```

## 🔧 AI Provider Library Installation

The AI provider libraries are optional and only needed if you plan to use the AI-powered demo:

### OpenAI
```bash
pip install openai>=1.0.0
```

### Anthropic Claude
```bash
pip install anthropic>=0.7.0
```

### Google Gemini
```bash
pip install google-generativeai>=0.3.0
```

### OpenRouter (uses requests)
```bash
pip install requests>=2.31.0
```

## 🐍 Python Version Requirements

- **Minimum Python Version**: 3.8+
- **Recommended Python Version**: 3.9+ or 3.10+
- **Tested Python Versions**: 3.9, 3.10, 3.11

## 📋 Dependency Details

### Core Framework Dependencies

#### Streamlit (>=1.28.0)
- **Purpose**: Web application framework for the demo interface
- **Why this version**: Includes latest caching improvements and UI components
- **Key features used**: st.cache_data, st.columns, st.expander, st.selectbox

#### Faker (>=19.0.0)
- **Purpose**: Generates realistic fake data for context services
- **Usage**: Creates customer profiles, addresses, names, and industry-specific data
- **Key providers used**: Person, Address, Company, Lorem, Date

### AI Provider Dependencies

#### OpenAI (>=1.0.0)
- **Purpose**: Access to GPT-3.5, GPT-4, and other OpenAI models
- **Breaking changes**: Version 1.0.0+ uses new client architecture
- **Configuration**: Requires OPENAI_API_KEY environment variable

#### Anthropic (>=0.7.0)
- **Purpose**: Access to Claude models (Claude-3 Opus, Sonnet, Haiku)
- **Configuration**: Requires ANTHROPIC_API_KEY environment variable
- **Features**: Supports system messages and long context windows

#### Google Generative AI (>=0.3.0)
- **Purpose**: Access to Gemini Pro and Gemini Ultra models
- **Configuration**: Requires GEMINI_API_KEY environment variable
- **Features**: Multimodal capabilities (text and image)

### Configuration Dependencies

#### Pydantic (>=2.0.0)
- **Purpose**: Data validation and settings management
- **Breaking changes**: Version 2.0+ has significant API changes from v1
- **Usage**: Validates AI configurations, application settings, and request/response models

#### Pydantic Settings (>=2.0.0)
- **Purpose**: Environment-based configuration management
- **Usage**: Loads settings from environment variables and .env files
- **Integration**: Works with Pydantic v2 for type-safe configuration

### Testing Dependencies

#### Pytest (>=7.0.0)
- **Purpose**: Core testing framework
- **Features**: Fixtures, parametrized tests, async support
- **Usage**: Unit tests, integration tests, and mocking

#### Responses (>=0.23.0)
- **Purpose**: HTTP request mocking for testing
- **Usage**: Mock AI provider API calls during testing
- **Benefits**: Enables testing without real API keys

## 🚨 Common Installation Issues

### Issue 1: AI Provider Library Import Errors

**Problem**: `ImportError: No module named 'openai'` or similar for other AI providers

**Solution**:
```bash
# Install the specific AI provider library
pip install openai>=1.0.0
pip install anthropic>=0.7.0
pip install google-generativeai>=0.3.0
```

**Note**: The application gracefully handles missing AI provider libraries and will show appropriate warnings.

### Issue 2: Pydantic Version Conflicts

**Problem**: `ImportError` or validation errors related to Pydantic

**Solution**:
```bash
# Ensure you have Pydantic v2
pip install --upgrade pydantic>=2.0.0 pydantic-settings>=2.0.0
```

### Issue 3: Streamlit Version Issues

**Problem**: Missing Streamlit features or caching errors

**Solution**:
```bash
# Upgrade to latest Streamlit
pip install --upgrade streamlit>=1.28.0
```

### Issue 4: Python Version Compatibility

**Problem**: Syntax errors or import issues

**Solution**:
```bash
# Check Python version
python --version

# Ensure you're using Python 3.8+
# Consider using pyenv or conda to manage Python versions
```

## 🔍 Dependency Validation

The application includes built-in dependency validation:

```bash
# Validate all dependencies and configuration
python validate_config.py

# Check specific components
python validate_openai.py
python validate_anthropic.py
```

## 📊 Performance Considerations

### Memory Usage
- **Base application**: ~50-100MB
- **With AI providers**: +50-200MB depending on loaded libraries
- **During AI calls**: +100-500MB for model inference

### Startup Time
- **Static demo**: ~2-5 seconds
- **AI-powered demo**: ~5-15 seconds (includes provider initialization)

### Caching
- **Streamlit caching**: Uses built-in `st.cache_data` (streamlit-cache is deprecated)
- **AI response caching**: Implemented in AI Service Orchestrator
- **Configuration caching**: Pydantic models cached at startup

## 🔄 Dependency Updates

### Updating Dependencies

```bash
# Update all dependencies to latest compatible versions
pip install --upgrade -r requirements.txt

# Update specific dependency
pip install --upgrade streamlit

# Check for outdated packages
pip list --outdated
```

### Version Pinning Strategy

- **Major versions**: Pinned to prevent breaking changes
- **Minor versions**: Minimum version specified for required features
- **Security updates**: Regular monitoring and updates recommended

## 🧪 Testing Dependencies

### Running Tests

```bash
# Install test dependencies
pip install pytest>=7.0.0 pytest-mock>=3.10.0 pytest-asyncio>=0.21.0 pytest-cov>=4.0.0 responses>=0.23.0

# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=config --cov=utils

# Run specific test categories
pytest tests/test_ai_service.py
pytest tests/test_*_provider.py
```

### Test Dependencies Explained

- **pytest-mock**: Provides `mocker` fixture for easy mocking
- **pytest-asyncio**: Enables testing of async AI provider calls
- **pytest-cov**: Generates code coverage reports
- **responses**: Mocks HTTP requests to AI provider APIs

## 🚀 Production Deployment

### Production Requirements

```bash
# Core production dependencies (minimal)
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
faker>=19.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
structlog>=23.0.0

# Add AI providers as needed
openai>=1.0.0
anthropic>=0.7.0
google-generativeai>=0.3.0
requests>=2.31.0
```

### Docker Considerations

```dockerfile
# Example Dockerfile snippet
FROM python:3.10-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
```

## 📝 Changelog

### Recent Changes (Latest)
- **Restructured requirements.txt**: Organized into logical sections with detailed comments
- **Added structlog**: Enhanced logging capabilities for better debugging
- **Added pytest-asyncio**: Support for testing async AI provider calls
- **Added pytest-cov**: Code coverage reporting for quality assurance
- **Added responses**: HTTP mocking for comprehensive AI provider testing
- **Removed streamlit-cache**: Deprecated, using built-in Streamlit caching
- **Updated version constraints**: Ensured compatibility with latest library versions

### Migration Notes
- **Pydantic v2**: Significant API changes from v1, all code updated accordingly
- **OpenAI v1.0+**: New client architecture, provider implementation updated
- **Streamlit 1.28+**: Improved caching system, legacy cache decorators removed

For more information about specific components, see:
- [AI Orchestrator Integration Guide](ai-orchestrator-integration.md)
- [Error Handling and Logging Guide](error-handling-and-logging.md)
- [Configuration Guide](configuration.md)
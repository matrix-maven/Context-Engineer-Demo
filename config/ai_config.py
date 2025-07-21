"""
AI provider configurations and settings using Pydantic.
"""
import os
from typing import Dict, Optional, List
from pydantic import BaseModel, Field, field_validator, SecretStr
from .settings import AIProvider


class AIConfig(BaseModel):
    """Configuration for AI providers with Pydantic validation."""
    provider: AIProvider = Field(..., description="AI provider type")
    api_key: SecretStr = Field(..., description="API key for the provider")
    model: str = Field(..., description="Model name to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Response temperature")
    max_tokens: int = Field(default=500, gt=0, description="Maximum response tokens")
    timeout: int = Field(default=30, gt=0, description="Request timeout in seconds")
    base_url: Optional[str] = Field(default=None, description="Custom base URL for API")
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        
    @field_validator('model')
    @classmethod
    def validate_model(cls, v):
        """Validate model name is not empty."""
        if not v or not v.strip():
            raise ValueError("Model name is required")
        return v.strip()
    
    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v):
        """Validate base URL format if provided."""
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError("Base URL must start with http:// or https://")
        return v
    
    def get_api_key(self) -> str:
        """Get the API key as a string."""
        return self.api_key.get_secret_value()


# Default model configurations for each provider
DEFAULT_MODELS = {
    AIProvider.OPENAI: "gpt-3.5-turbo",
    AIProvider.ANTHROPIC: "claude-3-haiku-20240307",
    AIProvider.GEMINI: "gemini-1.5-flash",
    AIProvider.OPENROUTER: "openai/gpt-3.5-turbo"
}

# Environment variable mappings
ENV_MAPPINGS = {
    AIProvider.OPENAI: {
        "api_key": "OPENAI_API_KEY",
        "model": "OPENAI_MODEL",
        "base_url": "OPENAI_BASE_URL"
    },
    AIProvider.ANTHROPIC: {
        "api_key": "ANTHROPIC_API_KEY", 
        "model": "ANTHROPIC_MODEL",
        "base_url": "ANTHROPIC_BASE_URL"
    },
    AIProvider.GEMINI: {
        "api_key": "GEMINI_API_KEY",
        "model": "GEMINI_MODEL", 
        "base_url": "GEMINI_BASE_URL"
    },
    AIProvider.OPENROUTER: {
        "api_key": "OPENROUTER_API_KEY",
        "model": "OPENROUTER_MODEL",
        "base_url": "OPENROUTER_BASE_URL"
    }
}


def load_ai_config(provider: AIProvider) -> Optional[AIConfig]:
    """Load AI configuration for a specific provider from environment variables."""
    env_mapping = ENV_MAPPINGS.get(provider)
    if not env_mapping:
        return None
    
    api_key = os.getenv(env_mapping["api_key"])
    if not api_key:
        return None  # Provider not configured
    
    model = os.getenv(env_mapping["model"], DEFAULT_MODELS[provider])
    base_url = os.getenv(env_mapping["base_url"])
    
    # Load global AI settings
    temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
    max_tokens = int(os.getenv("AI_MAX_TOKENS", "500"))
    timeout = int(os.getenv("AI_TIMEOUT", "30"))
    
    return AIConfig(
        provider=provider,
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        base_url=base_url
    )


def load_all_ai_configs() -> Dict[AIProvider, AIConfig]:
    """Load all available AI configurations."""
    configs = {}
    
    for provider in AIProvider:
        config = load_ai_config(provider)
        if config:
            configs[provider] = config
    
    return configs


def validate_ai_config(config: AIConfig) -> List[str]:
    """Validate AI configuration and return list of errors."""
    errors = []
    
    # Most validation is handled by Pydantic, but we can add custom business logic here
    try:
        # Test that we can get the API key
        api_key = config.get_api_key()
        if not api_key or len(api_key.strip()) == 0:
            errors.append(f"API key required for {config.provider.value}")
    except Exception as e:
        errors.append(f"Invalid API key for {config.provider.value}: {str(e)}")
    
    # Additional provider-specific validation could go here
    if config.provider == AIProvider.OPENAI and not config.model.startswith(('gpt-', 'text-', 'davinci')):
        errors.append(f"Invalid OpenAI model: {config.model}")
    elif config.provider == AIProvider.ANTHROPIC and not config.model.startswith('claude'):
        errors.append(f"Invalid Anthropic model: {config.model}")
    elif config.provider == AIProvider.GEMINI and not config.model.startswith('gemini'):
        errors.append(f"Invalid Gemini model: {config.model}")
    
    return errors


def get_available_providers() -> List[AIProvider]:
    """Get list of configured AI providers."""
    available = []
    
    for provider in AIProvider:
        config = load_ai_config(provider)
        if config:
            errors = validate_ai_config(config)
            if not errors:
                available.append(provider)
    
    return available


def get_default_provider() -> Optional[AIProvider]:
    """Get the default AI provider if available."""
    from .settings import get_settings
    
    settings = get_settings()
    default_provider = settings.default_ai_provider
    
    # Check if default provider is available
    available_providers = get_available_providers()
    if default_provider in available_providers:
        return default_provider
    
    # Return first available provider if default is not available
    return available_providers[0] if available_providers else None
"""
Application settings and configuration management using Pydantic.
"""
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class AIProvider(str, Enum):
    """Supported AI providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    OPENROUTER = "openrouter"


class AppSettings(BaseSettings):
    """Main application settings with Pydantic validation."""
    
    # Application settings
    app_title: str = Field(default="Context Engineering Demo", description="Application title", alias="APP_TITLE")
    app_icon: str = Field(default="🧠", description="Application icon")
    layout: str = Field(default="wide", description="Streamlit layout")
    
    # AI settings
    default_ai_provider: AIProvider = Field(default=AIProvider.OPENAI, description="Default AI provider", alias="AI_PROVIDER")
    ai_timeout: int = Field(default=30, gt=0, description="AI request timeout in seconds", alias="AI_TIMEOUT")
    ai_temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="AI response temperature", alias="AI_TEMPERATURE")
    ai_max_tokens: int = Field(default=500, gt=0, description="Maximum AI response tokens", alias="AI_MAX_TOKENS")
    
    # Performance settings
    enable_caching: bool = Field(default=True, description="Enable response caching", alias="ENABLE_CACHING")
    cache_ttl: int = Field(default=3600, gt=0, description="Cache TTL in seconds")
    
    # Logging settings
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level", alias="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    
    # Context settings
    max_context_size: int = Field(default=10000, gt=0, description="Maximum context size")
    context_refresh_interval: int = Field(default=300, gt=0, description="Context refresh interval in seconds")
    
    # UI settings
    industries: List[str] = Field(
        default_factory=lambda: [
            "Restaurant Reservations",
            "Healthcare", 
            "E-commerce",
            "Financial Services",
            "Education",
            "Real Estate"
        ],
        description="Available industries for demos"
    )
    
    # Development settings
    debug: bool = Field(default=False, description="Enable debug mode", alias="DEBUG")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }
    
    @field_validator('layout')
    @classmethod
    def validate_layout(cls, v):
        """Validate Streamlit layout options."""
        valid_layouts = ['centered', 'wide']
        if v not in valid_layouts:
            raise ValueError(f"Layout must be one of {valid_layouts}")
        return v
    
    @field_validator('industries')
    @classmethod
    def validate_industries(cls, v):
        """Validate industries list is not empty."""
        if not v or len(v) == 0:
            raise ValueError("Industries list cannot be empty")
        return v


# Global settings instance
_settings: Optional[AppSettings] = None


def get_settings() -> AppSettings:
    """Get the global settings instance with automatic validation."""
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings


def reload_settings() -> AppSettings:
    """Reload settings from environment (useful for testing)."""
    global _settings
    _settings = AppSettings()
    return _settings
"""
Configuration validation utilities and startup checks.
"""
import os
import sys
import logging
from typing import List, Dict, Optional, Tuple
from enum import Enum

from .settings import get_settings, AppSettings, AIProvider
from .ai_config import load_all_ai_configs, validate_ai_config, get_available_providers


class ValidationLevel(str, Enum):
    """Validation severity levels."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ValidationResult:
    """Result of configuration validation."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.is_valid: bool = True
    
    def add_error(self, message: str):
        """Add an error message."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)
    
    def add_info(self, message: str):
        """Add an info message."""
        self.info.append(message)
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0
    
    def get_summary(self) -> str:
        """Get a summary of validation results."""
        summary = []
        if self.errors:
            summary.append(f"{len(self.errors)} error(s)")
        if self.warnings:
            summary.append(f"{len(self.warnings)} warning(s)")
        if self.info:
            summary.append(f"{len(self.info)} info message(s)")
        
        if not summary:
            return "Configuration validation passed"
        
        return f"Validation completed with {', '.join(summary)}"


def validate_environment_variables() -> ValidationResult:
    """Validate required environment variables."""
    result = ValidationResult()
    
    # Check for at least one AI provider API key
    ai_keys = [
        ("OPENAI_API_KEY", "OpenAI"),
        ("ANTHROPIC_API_KEY", "Anthropic"),
        ("GEMINI_API_KEY", "Google Gemini"),
        ("OPENROUTER_API_KEY", "OpenRouter")
    ]
    
    configured_providers = []
    for env_var, provider_name in ai_keys:
        if os.getenv(env_var):
            configured_providers.append(provider_name)
            result.add_info(f"{provider_name} API key found")
        else:
            result.add_warning(f"{provider_name} API key not configured ({env_var})")
    
    if not configured_providers:
        result.add_error("No AI provider API keys configured. At least one is required.")
    else:
        result.add_info(f"Configured AI providers: {', '.join(configured_providers)}")
    
    # Validate numeric environment variables
    numeric_vars = [
        ("AI_TEMPERATURE", 0.0, 2.0),
        ("AI_MAX_TOKENS", 1, 4000),
        ("AI_TIMEOUT", 1, 300),
        ("CACHE_TTL", 60, 86400),
        ("MAX_CONTEXT_SIZE", 1000, 100000),
        ("CONTEXT_REFRESH_INTERVAL", 30, 3600)
    ]
    
    for var_name, min_val, max_val in numeric_vars:
        value = os.getenv(var_name)
        if value:
            try:
                num_value = float(value)
                if not (min_val <= num_value <= max_val):
                    result.add_warning(f"{var_name}={value} is outside recommended range [{min_val}, {max_val}]")
            except ValueError:
                result.add_error(f"{var_name}={value} is not a valid number")
    
    return result


def validate_ai_configuration() -> ValidationResult:
    """Validate AI provider configurations."""
    result = ValidationResult()
    
    try:
        # Load all AI configurations
        ai_configs = load_all_ai_configs()
        
        if not ai_configs:
            result.add_error("No valid AI provider configurations found")
            return result
        
        # Validate each configuration
        for provider, config in ai_configs.items():
            config_errors = validate_ai_config(config)
            if config_errors:
                for error in config_errors:
                    result.add_error(f"{provider.value}: {error}")
            else:
                result.add_info(f"{provider.value} configuration is valid")
        
        # Check if default provider is available
        available_providers = get_available_providers()
        settings = get_settings()
        
        if settings.default_ai_provider not in available_providers:
            if available_providers:
                result.add_warning(
                    f"Default provider '{settings.default_ai_provider.value}' not available. "
                    f"Will use '{available_providers[0].value}' instead."
                )
            else:
                result.add_error("No AI providers are available")
        else:
            result.add_info(f"Default AI provider '{settings.default_ai_provider.value}' is available")
    
    except Exception as e:
        result.add_error(f"Failed to validate AI configuration: {str(e)}")
    
    return result


def validate_application_settings() -> ValidationResult:
    """Validate application settings."""
    result = ValidationResult()
    
    try:
        settings = get_settings()
        
        # Validate industries list
        if not settings.industries:
            result.add_error("Industries list is empty")
        else:
            result.add_info(f"Configured {len(settings.industries)} industry demos")
        
        # Validate layout setting
        if settings.layout not in ['centered', 'wide']:
            result.add_error(f"Invalid layout setting: {settings.layout}")
        
        # Check debug mode in production
        if settings.debug and os.getenv('ENVIRONMENT') == 'production':
            result.add_warning("Debug mode is enabled in production environment")
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        if settings.log_level.value not in valid_log_levels:
            result.add_error(f"Invalid log level: {settings.log_level}")
        
        result.add_info("Application settings validation completed")
        
    except Exception as e:
        result.add_error(f"Failed to validate application settings: {str(e)}")
    
    return result


def validate_dependencies() -> ValidationResult:
    """Validate that required dependencies are installed."""
    result = ValidationResult()
    
    required_packages = [
        ('streamlit', 'Streamlit framework'),
        ('openai', 'OpenAI API client'),
        ('anthropic', 'Anthropic API client'),
        ('google.generativeai', 'Google Gemini API client'),
        ('faker', 'Faker data generation'),
        ('pydantic', 'Pydantic validation'),
        ('dotenv', 'Environment variable loading')
    ]
    
    for package, description in required_packages:
        try:
            __import__(package)
            result.add_info(f"{description} is available")
        except ImportError:
            result.add_warning(f"{description} is not installed ({package})")
    
    return result


def perform_startup_checks() -> ValidationResult:
    """Perform comprehensive startup validation checks."""
    result = ValidationResult()
    
    # Combine all validation results
    validations = [
        ("Environment Variables", validate_environment_variables()),
        ("AI Configuration", validate_ai_configuration()),
        ("Application Settings", validate_application_settings()),
        ("Dependencies", validate_dependencies())
    ]
    
    for check_name, check_result in validations:
        # Merge results
        result.errors.extend([f"{check_name}: {error}" for error in check_result.errors])
        result.warnings.extend([f"{check_name}: {warning}" for warning in check_result.warnings])
        result.info.extend([f"{check_name}: {info}" for info in check_result.info])
        
        if check_result.has_errors():
            result.is_valid = False
    
    return result


def setup_logging(settings: Optional[AppSettings] = None) -> None:
    """Set up application logging based on configuration."""
    if settings is None:
        settings = get_settings()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.value),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/app.log', mode='a') if os.path.exists('logs') else logging.NullHandler()
        ]
    )
    
    # Set up logger for this module
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {settings.log_level.value}")


def validate_and_setup() -> Tuple[bool, ValidationResult]:
    """
    Perform complete validation and setup.
    
    Returns:
        Tuple of (success: bool, validation_result: ValidationResult)
    """
    # Perform startup checks
    result = perform_startup_checks()
    
    # Setup logging
    try:
        setup_logging()
        result.add_info("Logging configured successfully")
    except Exception as e:
        result.add_error(f"Failed to setup logging: {str(e)}")
    
    return result.is_valid, result


def print_validation_results(result: ValidationResult, verbose: bool = False) -> None:
    """Print validation results to console."""
    print(f"\n{'='*60}")
    print("CONFIGURATION VALIDATION RESULTS")
    print(f"{'='*60}")
    
    if result.errors:
        print(f"\n❌ ERRORS ({len(result.errors)}):")
        for error in result.errors:
            print(f"   • {error}")
    
    if result.warnings:
        print(f"\n⚠️  WARNINGS ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"   • {warning}")
    
    if verbose and result.info:
        print(f"\n✅ INFO ({len(result.info)}):")
        for info in result.info:
            print(f"   • {info}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {result.get_summary()}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    """Run validation checks when executed directly."""
    success, validation_result = validate_and_setup()
    print_validation_results(validation_result, verbose=True)
    
    if not success:
        print("❌ Configuration validation failed. Please fix the errors above.")
        sys.exit(1)
    else:
        print("✅ Configuration validation passed successfully!")
        sys.exit(0)
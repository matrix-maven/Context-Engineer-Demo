"""
Error handling utilities and custom exceptions.
"""
import traceback
import time
import random
from typing import Dict, Any, Optional, Callable, TypeVar, Union
from enum import Enum
from functools import wraps
from .logger import get_logger

logger = get_logger("error_handler")

T = TypeVar('T')


class ErrorType(Enum):
    """Types of errors that can occur in the application."""
    AI_PROVIDER_ERROR = "ai_provider_error"
    CONFIGURATION_ERROR = "configuration_error"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"
    CONTEXT_ERROR = "context_error"
    UNKNOWN_ERROR = "unknown_error"


class ContextDemoError(Exception):
    """Base exception for Context Demo application."""
    
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN_ERROR, 
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_type = error_type
        self.context = context or {}
        self.message = message


class AIProviderError(ContextDemoError):
    """Exception for AI provider related errors."""
    
    def __init__(self, message: str, provider: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorType.AI_PROVIDER_ERROR, context)
        self.provider = provider


class ConfigurationError(ContextDemoError):
    """Exception for configuration related errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorType.CONFIGURATION_ERROR, context)


class NetworkError(ContextDemoError):
    """Exception for network related errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorType.NETWORK_ERROR, context)


class ValidationError(ContextDemoError):
    """Exception for validation related errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorType.VALIDATION_ERROR, context)


class ContextError(ContextDemoError):
    """Exception for context generation related errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorType.CONTEXT_ERROR, context)


class RetryConfig:
    """Configuration for retry logic."""
    
    def __init__(self, 
                 max_retries: int = 3,
                 base_delay: float = 1.0,
                 max_delay: float = 60.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter


def retry_with_exponential_backoff(
    retry_config: Optional[RetryConfig] = None,
    exceptions: tuple = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for implementing retry logic with exponential backoff.
    
    Args:
        retry_config: Retry configuration
        exceptions: Tuple of exceptions to retry on
        on_retry: Callback function called on each retry attempt
        
    Returns:
        Decorated function with retry logic
    """
    if retry_config is None:
        retry_config = RetryConfig()
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(retry_config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == retry_config.max_retries:
                        # Final attempt failed, raise the exception
                        logger.error(f"Function {func.__name__} failed after {retry_config.max_retries + 1} attempts: {e}")
                        raise e
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        retry_config.base_delay * (retry_config.exponential_base ** attempt),
                        retry_config.max_delay
                    )
                    
                    # Add jitter to prevent thundering herd
                    if retry_config.jitter:
                        delay *= (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{retry_config.max_retries + 1}): {e}. Retrying in {delay:.2f}s")
                    
                    # Call retry callback if provided
                    if on_retry:
                        on_retry(e, attempt + 1)
                    
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            if last_exception:
                raise last_exception
            
        return wrapper
    return decorator


class ErrorHandler:
    """Centralized error handling for the application."""
    
    @staticmethod
    def handle_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> str:
        """Handle an error and return a user-friendly message."""
        error_context = context or {}
        
        # Log the full error details
        logger.error(
            f"Error occurred: {str(error)}",
            extra={
                "error_type": getattr(error, 'error_type', ErrorType.UNKNOWN_ERROR).value,
                "context": error_context,
                "traceback": traceback.format_exc()
            }
        )
        
        # Return user-friendly message based on error type
        if isinstance(error, AIProviderError):
            return ErrorHandler._handle_ai_provider_error(error)
        elif isinstance(error, ConfigurationError):
            return ErrorHandler._handle_configuration_error(error)
        elif isinstance(error, NetworkError):
            return ErrorHandler._handle_network_error(error)
        elif isinstance(error, ValidationError):
            return ErrorHandler._handle_validation_error(error)
        elif isinstance(error, ContextError):
            return ErrorHandler._handle_context_error(error)
        else:
            return ErrorHandler._handle_unknown_error(error)
    
    @staticmethod
    def _handle_ai_provider_error(error: AIProviderError) -> str:
        """Handle AI provider specific errors."""
        if "rate limit" in error.message.lower():
            return f"⚠️ The {error.provider} service is currently busy. Please try again in a moment."
        elif "authentication" in error.message.lower() or "api key" in error.message.lower():
            return f"🔑 There's an issue with the {error.provider} API configuration. Please check your settings."
        elif "timeout" in error.message.lower():
            return f"⏱️ The {error.provider} service is taking too long to respond. Please try again."
        else:
            return f"❌ Unable to get response from {error.provider}. Please try a different provider or try again later."
    
    @staticmethod
    def _handle_configuration_error(error: ConfigurationError) -> str:
        """Handle configuration specific errors."""
        return f"⚙️ Configuration issue: {error.message}. Please check your settings."
    
    @staticmethod
    def _handle_network_error(error: NetworkError) -> str:
        """Handle network specific errors."""
        return "🌐 Network connection issue. Please check your internet connection and try again."
    
    @staticmethod
    def _handle_validation_error(error: ValidationError) -> str:
        """Handle validation specific errors."""
        return f"📝 Input validation error: {error.message}"
    
    @staticmethod
    def _handle_context_error(error: ContextError) -> str:
        """Handle context generation specific errors."""
        return f"🔄 Context generation issue: {error.message}. Using fallback data."
    
    @staticmethod
    def _handle_unknown_error(error: Exception) -> str:
        """Handle unknown errors."""
        return "❌ An unexpected error occurred. Please try again or contact support if the issue persists."
    
    @staticmethod
    def get_fallback_response(query: str, industry: str) -> str:
        """Get a fallback response when AI providers are unavailable."""
        return f"""🤖 **Fallback Response for {industry}**

I'm currently unable to provide AI-powered responses, but here's some general guidance for your query: "{query}"

**General Recommendations:**
- Consider your specific needs and preferences
- Look for options that match your requirements
- Compare different alternatives available
- Seek additional information if needed

**Note:** This is a fallback response. AI-powered responses will provide more personalized and detailed assistance once the service is restored."""
    
    @staticmethod
    def handle_ai_provider_failure(provider: str, error: Exception, 
                                 fallback_providers: Optional[list] = None) -> Dict[str, Any]:
        """
        Handle AI provider failure with fallback logic.
        
        Args:
            provider: Name of the failed provider
            error: The exception that occurred
            fallback_providers: List of alternative providers to try
            
        Returns:
            Dictionary with error info and fallback suggestions
        """
        error_info = {
            'failed_provider': provider,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': time.time(),
            'fallback_available': bool(fallback_providers),
            'suggested_fallbacks': fallback_providers or []
        }
        
        logger.error(f"AI provider {provider} failed: {error}", extra=error_info)
        
        return error_info
    
    @staticmethod
    def create_circuit_breaker(failure_threshold: int = 5, 
                             recovery_timeout: int = 60) -> Callable:
        """
        Create a circuit breaker for AI provider calls.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time in seconds before attempting recovery
            
        Returns:
            Circuit breaker decorator
        """
        failure_count = 0
        last_failure_time = 0
        circuit_open = False
        
        def circuit_breaker(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal failure_count, last_failure_time, circuit_open
                
                current_time = time.time()
                
                # Check if circuit should be closed (recovery attempt)
                if circuit_open and (current_time - last_failure_time) > recovery_timeout:
                    circuit_open = False
                    failure_count = 0
                    logger.info(f"Circuit breaker for {func.__name__} attempting recovery")
                
                # If circuit is open, fail fast
                if circuit_open:
                    raise AIProviderError(
                        f"Circuit breaker is open for {func.__name__}. "
                        f"Will retry after {recovery_timeout - (current_time - last_failure_time):.0f}s",
                        "circuit_breaker"
                    )
                
                try:
                    result = func(*args, **kwargs)
                    # Success - reset failure count
                    failure_count = 0
                    return result
                    
                except Exception as e:
                    failure_count += 1
                    last_failure_time = current_time
                    
                    # Open circuit if threshold reached
                    if failure_count >= failure_threshold:
                        circuit_open = True
                        logger.warning(f"Circuit breaker opened for {func.__name__} after {failure_count} failures")
                    
                    raise e
            
            return wrapper
        return circuit_breaker
    
    @staticmethod
    def log_performance_metrics(func_name: str, execution_time: float, 
                              success: bool, error: Optional[Exception] = None) -> None:
        """
        Log performance metrics for function calls.
        
        Args:
            func_name: Name of the function
            execution_time: Time taken to execute
            success: Whether the function succeeded
            error: Exception if function failed
        """
        metrics = {
            'function': func_name,
            'execution_time': execution_time,
            'success': success,
            'timestamp': time.time()
        }
        
        if error:
            metrics['error_type'] = type(error).__name__
            metrics['error_message'] = str(error)
        
        if success:
            logger.info(f"Function {func_name} completed successfully in {execution_time:.3f}s", extra=metrics)
        else:
            logger.warning(f"Function {func_name} failed after {execution_time:.3f}s", extra=metrics)
    
    @staticmethod
    def safe_execute(func: Callable, *args, default_return=None, 
                    log_errors: bool = True, **kwargs) -> Any:
        """
        Safely execute a function with error handling.
        
        Args:
            func: Function to execute
            *args: Function arguments
            default_return: Default value to return on error
            log_errors: Whether to log errors
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or default_return on error
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if log_errors:
                logger.error(f"Safe execution of {func.__name__} failed: {e}")
            return default_return
    
    @staticmethod
    def validate_and_sanitize_input(input_data: Any, 
                                  validation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize input data.
        
        Args:
            input_data: Data to validate
            validation_rules: Dictionary of validation rules
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': True,
            'errors': [],
            'sanitized_data': input_data,
            'warnings': []
        }
        
        try:
            # Basic validation rules
            if 'required_fields' in validation_rules:
                for field in validation_rules['required_fields']:
                    if not hasattr(input_data, field) and field not in input_data:
                        result['valid'] = False
                        result['errors'].append(f"Required field '{field}' is missing")
            
            if 'max_length' in validation_rules:
                for field, max_len in validation_rules['max_length'].items():
                    if hasattr(input_data, field):
                        value = getattr(input_data, field)
                        if isinstance(value, str) and len(value) > max_len:
                            result['warnings'].append(f"Field '{field}' exceeds maximum length of {max_len}")
                            # Truncate the value
                            setattr(input_data, field, value[:max_len])
            
            if 'allowed_values' in validation_rules:
                for field, allowed in validation_rules['allowed_values'].items():
                    if hasattr(input_data, field):
                        value = getattr(input_data, field)
                        if value not in allowed:
                            result['valid'] = False
                            result['errors'].append(f"Field '{field}' has invalid value. Allowed: {allowed}")
            
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Validation error: {str(e)}")
            logger.error(f"Input validation failed: {e}")
        
        return result


def handle_startup_errors() -> Optional[str]:
    """Check for startup configuration errors and return error message if any."""
    try:
        from config.settings import get_settings
        from config.ai_config import get_available_providers
        
        # Validate settings
        settings = get_settings()
        
        # Check if at least one AI provider is configured
        available_providers = get_available_providers()
        if not available_providers:
            return """⚠️ **Configuration Required**
            
No AI providers are configured. Please set up at least one of the following:

- **OpenAI**: Set `OPENAI_API_KEY` environment variable
- **Anthropic**: Set `ANTHROPIC_API_KEY` environment variable  
- **Gemini**: Set `GEMINI_API_KEY` environment variable
- **OpenRouter**: Set `OPENROUTER_API_KEY` environment variable

The application will use fallback responses until an AI provider is configured."""
        
        return None  # No startup errors
        
    except Exception as e:
        logger.error(f"Startup validation failed: {str(e)}")
        return f"❌ **Startup Error**: {str(e)}"
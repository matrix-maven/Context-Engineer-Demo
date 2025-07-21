"""
Tests for error handling utilities.
"""
import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from utils.error_handler import (
    ErrorHandler, ErrorType, ContextDemoError, AIProviderError,
    ConfigurationError, NetworkError, ValidationError, ContextError,
    RetryConfig, retry_with_exponential_backoff, handle_startup_errors
)


class TestErrorHandler:
    """Test cases for ErrorHandler class."""
    
    def test_handle_ai_provider_error_rate_limit(self):
        """Test handling of AI provider rate limit errors."""
        error = AIProviderError("Rate limit exceeded", "openai")
        result = ErrorHandler.handle_error(error)
        
        assert "busy" in result.lower()
        assert "openai" in result.lower()
        assert "⚠️" in result
    
    def test_handle_ai_provider_error_authentication(self):
        """Test handling of AI provider authentication errors."""
        error = AIProviderError("Invalid API key", "anthropic")
        result = ErrorHandler.handle_error(error)
        
        assert "api" in result.lower()
        assert "anthropic" in result.lower()
        assert "🔑" in result
    
    def test_handle_ai_provider_error_timeout(self):
        """Test handling of AI provider timeout errors."""
        error = AIProviderError("Request timeout", "gemini")
        result = ErrorHandler.handle_error(error)
        
        assert "timeout" in result.lower() or "long" in result.lower()
        assert "gemini" in result.lower()
        assert "⏱️" in result
    
    def test_handle_configuration_error(self):
        """Test handling of configuration errors."""
        error = ConfigurationError("Missing required setting")
        result = ErrorHandler.handle_error(error)
        
        assert "configuration" in result.lower()
        assert "⚙️" in result
    
    def test_handle_network_error(self):
        """Test handling of network errors."""
        error = NetworkError("Connection failed")
        result = ErrorHandler.handle_error(error)
        
        assert "network" in result.lower()
        assert "🌐" in result
    
    def test_handle_validation_error(self):
        """Test handling of validation errors."""
        error = ValidationError("Invalid input format")
        result = ErrorHandler.handle_error(error)
        
        assert "validation" in result.lower()
        assert "📝" in result
    
    def test_handle_context_error(self):
        """Test handling of context generation errors."""
        error = ContextError("Failed to generate context")
        result = ErrorHandler.handle_error(error)
        
        assert "context" in result.lower()
        assert "🔄" in result
    
    def test_handle_unknown_error(self):
        """Test handling of unknown errors."""
        error = Exception("Unknown error")
        result = ErrorHandler.handle_error(error)
        
        assert "unexpected" in result.lower()
        assert "❌" in result
    
    def test_get_fallback_response(self):
        """Test fallback response generation."""
        query = "How to optimize performance?"
        industry = "healthcare"
        
        result = ErrorHandler.get_fallback_response(query, industry)
        
        assert query in result
        assert industry in result
        assert "Fallback Response" in result
        assert "🤖" in result
    
    def test_handle_ai_provider_failure(self):
        """Test AI provider failure handling."""
        provider = "openai"
        error = Exception("API error")
        fallback_providers = ["anthropic", "gemini"]
        
        result = ErrorHandler.handle_ai_provider_failure(provider, error, fallback_providers)
        
        assert result['failed_provider'] == provider
        assert result['error_type'] == "Exception"
        assert result['fallback_available'] is True
        assert result['suggested_fallbacks'] == fallback_providers
    
    def test_create_circuit_breaker(self):
        """Test circuit breaker creation and functionality."""
        failure_count = 0
        
        @ErrorHandler.create_circuit_breaker(failure_threshold=2, recovery_timeout=1)
        def failing_function():
            nonlocal failure_count
            failure_count += 1
            if failure_count <= 2:
                raise Exception("Simulated failure")
            return "success"
        
        # First two calls should fail
        with pytest.raises(Exception):
            failing_function()
        
        with pytest.raises(Exception):
            failing_function()
        
        # Third call should trigger circuit breaker
        with pytest.raises(AIProviderError) as exc_info:
            failing_function()
        
        assert "Circuit breaker is open" in str(exc_info.value)
    
    def test_safe_execute_success(self):
        """Test safe execution with successful function."""
        def successful_function(x, y):
            return x + y
        
        result = ErrorHandler.safe_execute(successful_function, 2, 3)
        assert result == 5
    
    def test_safe_execute_failure(self):
        """Test safe execution with failing function."""
        def failing_function():
            raise Exception("Test error")
        
        result = ErrorHandler.safe_execute(failing_function, default_return="fallback")
        assert result == "fallback"
    
    def test_validate_and_sanitize_input_valid(self):
        """Test input validation with valid data."""
        input_data = {"name": "test", "value": 42}
        validation_rules = {
            "required_fields": ["name", "value"],
            "max_length": {"name": 10},
            "allowed_values": {"value": [42, 100]}
        }
        
        result = ErrorHandler.validate_and_sanitize_input(input_data, validation_rules)
        
        assert result['valid'] is True
        assert len(result['errors']) == 0
    
    def test_validate_and_sanitize_input_invalid(self):
        """Test input validation with invalid data."""
        input_data = {"name": "test"}
        validation_rules = {
            "required_fields": ["name", "value"]
        }
        
        result = ErrorHandler.validate_and_sanitize_input(input_data, validation_rules)
        
        assert result['valid'] is False
        assert len(result['errors']) > 0
        assert "Required field 'value' is missing" in result['errors'][0]


class TestRetryDecorator:
    """Test cases for retry decorator."""
    
    def test_retry_success_on_first_attempt(self):
        """Test retry decorator with successful first attempt."""
        call_count = 0
        
        @retry_with_exponential_backoff(RetryConfig(max_retries=3))
        def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = successful_function()
        
        assert result == "success"
        assert call_count == 1
    
    def test_retry_success_after_failures(self):
        """Test retry decorator with success after failures."""
        call_count = 0
        
        @retry_with_exponential_backoff(RetryConfig(max_retries=3, base_delay=0.01))
        def eventually_successful_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        result = eventually_successful_function()
        
        assert result == "success"
        assert call_count == 3
    
    def test_retry_max_retries_exceeded(self):
        """Test retry decorator when max retries are exceeded."""
        call_count = 0
        
        @retry_with_exponential_backoff(RetryConfig(max_retries=2, base_delay=0.01))
        def always_failing_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError):
            always_failing_function()
        
        assert call_count == 3  # Initial attempt + 2 retries
    
    def test_retry_with_specific_exceptions(self):
        """Test retry decorator with specific exception types."""
        call_count = 0
        
        @retry_with_exponential_backoff(
            RetryConfig(max_retries=2, base_delay=0.01),
            exceptions=(ValueError,)
        )
        def function_with_different_errors():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("Retryable error")
            elif call_count == 2:
                raise TypeError("Non-retryable error")
            return "success"
        
        with pytest.raises(TypeError):
            function_with_different_errors()
        
        assert call_count == 2
    
    def test_retry_with_callback(self):
        """Test retry decorator with retry callback."""
        retry_attempts = []
        
        def on_retry(error, attempt):
            retry_attempts.append((str(error), attempt))
        
        @retry_with_exponential_backoff(
            RetryConfig(max_retries=2, base_delay=0.01),
            on_retry=on_retry
        )
        def failing_function():
            raise Exception("Test error")
        
        with pytest.raises(Exception):
            failing_function()
        
        assert len(retry_attempts) == 2
        assert retry_attempts[0][1] == 1
        assert retry_attempts[1][1] == 2


class TestStartupErrorHandling:
    """Test cases for startup error handling."""
    
    @patch('config.settings.get_settings')
    @patch('config.ai_config.get_available_providers')
    def test_handle_startup_errors_no_providers(self, mock_get_providers, mock_get_settings):
        """Test startup error handling when no providers are configured."""
        mock_get_settings.return_value = Mock()
        mock_get_providers.return_value = []
        
        result = handle_startup_errors()
        
        assert result is not None
        assert "No AI providers are configured" in result
        assert "OPENAI_API_KEY" in result
    
    @patch('config.settings.get_settings')
    @patch('config.ai_config.get_available_providers')
    def test_handle_startup_errors_providers_available(self, mock_get_providers, mock_get_settings):
        """Test startup error handling when providers are available."""
        mock_get_settings.return_value = Mock()
        mock_get_providers.return_value = ["openai", "anthropic"]
        
        result = handle_startup_errors()
        
        assert result is None
    
    @patch('config.settings.get_settings')
    def test_handle_startup_errors_exception(self, mock_get_settings):
        """Test startup error handling when an exception occurs."""
        mock_get_settings.side_effect = Exception("Configuration error")
        
        result = handle_startup_errors()
        
        assert result is not None
        assert "Startup Error" in result
        assert "Configuration error" in result


class TestCustomExceptions:
    """Test cases for custom exception classes."""
    
    def test_context_demo_error(self):
        """Test ContextDemoError base exception."""
        error = ContextDemoError("Test message", ErrorType.UNKNOWN_ERROR, {"key": "value"})
        
        assert str(error) == "Test message"
        assert error.error_type == ErrorType.UNKNOWN_ERROR
        assert error.context == {"key": "value"}
        assert error.message == "Test message"
    
    def test_ai_provider_error(self):
        """Test AIProviderError exception."""
        error = AIProviderError("API error", "openai", {"request_id": "123"})
        
        assert str(error) == "API error"
        assert error.error_type == ErrorType.AI_PROVIDER_ERROR
        assert error.provider == "openai"
        assert error.context == {"request_id": "123"}
    
    def test_configuration_error(self):
        """Test ConfigurationError exception."""
        error = ConfigurationError("Missing config", {"setting": "api_key"})
        
        assert str(error) == "Missing config"
        assert error.error_type == ErrorType.CONFIGURATION_ERROR
        assert error.context == {"setting": "api_key"}
    
    def test_network_error(self):
        """Test NetworkError exception."""
        error = NetworkError("Connection timeout")
        
        assert str(error) == "Connection timeout"
        assert error.error_type == ErrorType.NETWORK_ERROR
    
    def test_validation_error(self):
        """Test ValidationError exception."""
        error = ValidationError("Invalid format")
        
        assert str(error) == "Invalid format"
        assert error.error_type == ErrorType.VALIDATION_ERROR
    
    def test_context_error(self):
        """Test ContextError exception."""
        error = ContextError("Generation failed")
        
        assert str(error) == "Generation failed"
        assert error.error_type == ErrorType.CONTEXT_ERROR


if __name__ == "__main__":
    pytest.main([__file__])
"""
Unit tests for AI service infrastructure.
"""
import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch
from typing import Dict, Any

from services.ai_service import (
    AIResponse, PromptRequest, BaseAIProvider, ResponseStatus,
    AIProviderError, AIProviderTimeoutError, AIProviderRateLimitError,
    AIProviderAuthenticationError, AIProviderInvalidRequestError
)
from config.ai_config import AIConfig
from config.settings import AIProvider


class TestAIResponse:
    """Test cases for AIResponse data model."""
    
    def test_ai_response_creation(self):
        """Test basic AIResponse creation."""
        response = AIResponse(
            content="Test response",
            provider=AIProvider.OPENAI,
            model="gpt-3.5-turbo",
            status=ResponseStatus.SUCCESS,
            tokens_used=50,
            response_time=1.5
        )
        
        assert response.content == "Test response"
        assert response.provider == AIProvider.OPENAI
        assert response.model == "gpt-3.5-turbo"
        assert response.status == ResponseStatus.SUCCESS
        assert response.tokens_used == 50
        assert response.response_time == 1.5
        assert response.success is True
        assert response.has_error is False
        assert isinstance(response.timestamp, datetime)
    
    def test_ai_response_error(self):
        """Test AIResponse with error status."""
        response = AIResponse(
            content="",
            provider=AIProvider.OPENAI,
            model="gpt-3.5-turbo",
            status=ResponseStatus.ERROR,
            error_message="API error",
            error_code="500"
        )
        
        assert response.success is False
        assert response.has_error is True
        assert response.error_message == "API error"
        assert response.error_code == "500"
    
    def test_ai_response_to_dict(self):
        """Test AIResponse serialization to dictionary."""
        timestamp = datetime.now(timezone.utc)
        response = AIResponse(
            content="Test response",
            provider=AIProvider.OPENAI,
            model="gpt-3.5-turbo",
            status=ResponseStatus.SUCCESS,
            tokens_used=50,
            response_time=1.5,
            timestamp=timestamp,
            metadata={"test": "value"}
        )
        
        result = response.to_dict()
        
        assert result['content'] == "Test response"
        assert result['provider'] == "openai"
        assert result['model'] == "gpt-3.5-turbo"
        assert result['status'] == "success"
        assert result['tokens_used'] == 50
        assert result['response_time'] == 1.5
        assert result['timestamp'] == timestamp.isoformat()
        assert result['metadata'] == {"test": "value"}


class TestPromptRequest:
    """Test cases for PromptRequest data model."""
    
    def test_prompt_request_creation(self):
        """Test basic PromptRequest creation."""
        request = PromptRequest(
            prompt="Test prompt",
            context={"user": "test"},
            temperature=0.8,
            max_tokens=100,
            system_message="You are a helpful assistant"
        )
        
        assert request.prompt == "Test prompt"
        assert request.context == {"user": "test"}
        assert request.temperature == 0.8
        assert request.max_tokens == 100
        assert request.system_message == "You are a helpful assistant"
    
    def test_prompt_request_minimal(self):
        """Test PromptRequest with minimal parameters."""
        request = PromptRequest(prompt="Test prompt")
        
        assert request.prompt == "Test prompt"
        assert request.context is None
        assert request.temperature is None
        assert request.max_tokens is None
        assert request.system_message is None
        assert request.metadata is None
    
    def test_prompt_request_to_dict(self):
        """Test PromptRequest serialization to dictionary."""
        request = PromptRequest(
            prompt="Test prompt",
            context={"user": "test"},
            temperature=0.8,
            max_tokens=100,
            metadata={"test": "value"}
        )
        
        result = request.to_dict()
        
        assert result['prompt'] == "Test prompt"
        assert result['context'] == {"user": "test"}
        assert result['temperature'] == 0.8
        assert result['max_tokens'] == 100
        assert result['metadata'] == {"test": "value"}


class TestAIProviderErrors:
    """Test cases for AI provider error classes."""
    
    def test_ai_provider_error(self):
        """Test basic AIProviderError."""
        error = AIProviderError(
            "Test error",
            error_code="TEST_001",
            provider=AIProvider.OPENAI
        )
        
        assert str(error) == "Test error"
        assert error.error_code == "TEST_001"
        assert error.provider == AIProvider.OPENAI
        assert isinstance(error.timestamp, datetime)
    
    def test_ai_provider_timeout_error(self):
        """Test AIProviderTimeoutError."""
        error = AIProviderTimeoutError("Request timed out")
        
        assert str(error) == "Request timed out"
        assert isinstance(error, AIProviderError)
    
    def test_ai_provider_rate_limit_error(self):
        """Test AIProviderRateLimitError."""
        error = AIProviderRateLimitError("Rate limit exceeded")
        
        assert str(error) == "Rate limit exceeded"
        assert isinstance(error, AIProviderError)
    
    def test_ai_provider_authentication_error(self):
        """Test AIProviderAuthenticationError."""
        error = AIProviderAuthenticationError("Invalid API key")
        
        assert str(error) == "Invalid API key"
        assert isinstance(error, AIProviderError)
    
    def test_ai_provider_invalid_request_error(self):
        """Test AIProviderInvalidRequestError."""
        error = AIProviderInvalidRequestError("Invalid request format")
        
        assert str(error) == "Invalid request format"
        assert isinstance(error, AIProviderError)


class MockAIProvider(BaseAIProvider):
    """Mock AI provider for testing."""
    
    def _validate_config(self) -> None:
        """Mock validation - always passes."""
        pass
    
    def generate_response(self, request: PromptRequest) -> AIResponse:
        """Mock response generation."""
        return AIResponse(
            content=f"Mock response to: {request.prompt}",
            provider=self.config.provider,
            model=self.config.model,
            status=ResponseStatus.SUCCESS,
            tokens_used=25,
            response_time=0.5
        )
    
    def validate_connection(self) -> bool:
        """Mock connection validation."""
        return True
    
    def get_model_info(self) -> Dict[str, Any]:
        """Mock model info."""
        return {
            "name": self.config.model,
            "provider": self.config.provider.value,
            "max_tokens": self.config.max_tokens
        }


class TestBaseAIProvider:
    """Test cases for BaseAIProvider abstract class."""
    
    @pytest.fixture
    def ai_config(self):
        """Create test AI configuration."""
        return AIConfig(
            provider=AIProvider.OPENAI,
            api_key="test-key",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
    
    @pytest.fixture
    def mock_provider(self, ai_config):
        """Create mock AI provider."""
        return MockAIProvider(ai_config)
    
    def test_provider_initialization(self, ai_config):
        """Test provider initialization."""
        provider = MockAIProvider(ai_config)
        
        assert provider.config == ai_config
        assert provider.logger.name == "MockAIProvider"
    
    def test_create_error_response(self, mock_provider):
        """Test error response creation."""
        error = AIProviderTimeoutError("Request timed out")
        request = PromptRequest(prompt="Test prompt")
        
        response = mock_provider.create_error_response(error, request)
        
        assert response.status == ResponseStatus.TIMEOUT
        assert response.error_message == "Request timed out"
        assert response.provider == AIProvider.OPENAI
        assert response.model == "gpt-3.5-turbo"
        assert response.content == ""
        assert response.metadata['request']['prompt'] == "Test prompt"
    
    def test_create_error_response_different_errors(self, mock_provider):
        """Test error response creation for different error types."""
        test_cases = [
            (AIProviderRateLimitError("Rate limited"), ResponseStatus.RATE_LIMITED),
            (AIProviderInvalidRequestError("Invalid"), ResponseStatus.INVALID_REQUEST),
            (AIProviderError("Generic error"), ResponseStatus.ERROR),
            (Exception("Unknown error"), ResponseStatus.ERROR)
        ]
        
        for error, expected_status in test_cases:
            response = mock_provider.create_error_response(error)
            assert response.status == expected_status
            assert response.error_message == str(error)
    
    def test_measure_response_time(self, mock_provider):
        """Test response time measurement."""
        def slow_function():
            import time
            time.sleep(0.1)
            return "result"
        
        result, response_time = mock_provider._measure_response_time(slow_function)
        
        assert result == "result"
        assert response_time >= 0.1
        assert response_time < 0.2  # Should be close to 0.1 seconds
    
    def test_measure_response_time_with_exception(self, mock_provider):
        """Test response time measurement when function raises exception."""
        def failing_function():
            import time
            time.sleep(0.1)
            raise AIProviderError("Test error")
        
        with pytest.raises(AIProviderError) as exc_info:
            mock_provider._measure_response_time(failing_function)
        
        # Check that response time was added to error metadata
        error = exc_info.value
        assert hasattr(error, 'metadata')
        assert 'response_time' in error.metadata
        assert error.metadata['response_time'] >= 0.1
    
    def test_log_request(self, mock_provider):
        """Test request logging."""
        with patch.object(mock_provider.logger, 'debug') as mock_debug:
            request = PromptRequest(
                prompt="Test prompt",
                context={"user": "test"}
            )
            
            mock_provider._log_request(request)
            
            # Verify logger was called with correct parameters
            mock_debug.assert_called_once()
            call_args = mock_debug.call_args[0][0]
            assert "AI request to openai" in call_args
            assert "model=gpt-3.5-turbo" in call_args
            assert "prompt_length=11" in call_args
            assert "has_context=True" in call_args
    
    def test_log_response_success(self, mock_provider):
        """Test successful response logging."""
        with patch.object(mock_provider.logger, 'debug') as mock_debug:
            response = AIResponse(
                content="Test response",
                provider=AIProvider.OPENAI,
                model="gpt-3.5-turbo",
                status=ResponseStatus.SUCCESS,
                tokens_used=25,
                response_time=1.5
            )
            
            mock_provider._log_response(response)
            
            mock_debug.assert_called_once()
            call_args = mock_debug.call_args[0][0]
            assert "AI response from openai" in call_args
            assert "status=success" in call_args
            assert "tokens=25" in call_args
            assert "time=1.50s" in call_args
    
    def test_log_response_error(self, mock_provider):
        """Test error response logging."""
        with patch.object(mock_provider.logger, 'warning') as mock_warning:
            response = AIResponse(
                content="",
                provider=AIProvider.OPENAI,
                model="gpt-3.5-turbo",
                status=ResponseStatus.ERROR,
                error_message="API error"
            )
            
            mock_provider._log_response(response)
            
            mock_warning.assert_called_once()
            call_args = mock_warning.call_args[0][0]
            assert "AI error from openai" in call_args
            assert "status=error" in call_args
            assert "error=API error" in call_args
    
    def test_string_representations(self, mock_provider):
        """Test string representations of provider."""
        str_repr = str(mock_provider)
        assert "MockAIProvider" in str_repr
        assert "provider=openai" in str_repr
        assert "model=gpt-3.5-turbo" in str_repr
        
        repr_str = repr(mock_provider)
        assert "MockAIProvider" in repr_str
        assert "provider=openai" in repr_str
        assert "model=gpt-3.5-turbo" in repr_str
        assert "temperature=0.7" in repr_str
        assert "max_tokens=500" in repr_str
    
    def test_abstract_methods_must_be_implemented(self, ai_config):
        """Test that abstract methods must be implemented."""
        with pytest.raises(TypeError):
            # This should fail because BaseAIProvider is abstract
            BaseAIProvider(ai_config)
    
    def test_mock_provider_methods(self, mock_provider):
        """Test mock provider implementation."""
        # Test generate_response
        request = PromptRequest(prompt="Test prompt")
        response = mock_provider.generate_response(request)
        
        assert response.content == "Mock response to: Test prompt"
        assert response.status == ResponseStatus.SUCCESS
        assert response.tokens_used == 25
        assert response.response_time == 0.5
        
        # Test validate_connection
        assert mock_provider.validate_connection() is True
        
        # Test get_model_info
        model_info = mock_provider.get_model_info()
        assert model_info['name'] == "gpt-3.5-turbo"
        assert model_info['provider'] == "openai"
        assert model_info['max_tokens'] == 500


if __name__ == "__main__":
    pytest.main([__file__])
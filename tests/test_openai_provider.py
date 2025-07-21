"""
Unit tests for OpenAI provider implementation.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import json

# Import the classes we're testing
from services.openai_provider import OpenAIProvider, OPENAI_AVAILABLE
from services.ai_service import (
    AIResponse, PromptRequest, ResponseStatus,
    AIProviderError, AIProviderTimeoutError, AIProviderRateLimitError,
    AIProviderAuthenticationError, AIProviderInvalidRequestError
)
from config.ai_config import AIConfig
from config.settings import AIProvider


# Test fixtures
@pytest.fixture
def valid_config():
    """Create a valid OpenAI configuration for testing."""
    return AIConfig(
        provider=AIProvider.OPENAI,
        api_key="test-api-key-12345",
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500,
        timeout=30
    )


@pytest.fixture
def invalid_config():
    """Create an invalid configuration for testing."""
    return AIConfig(
        provider=AIProvider.ANTHROPIC,  # Wrong provider
        api_key="test-api-key",
        model="claude-3-haiku",
        temperature=0.7,
        max_tokens=500,
        timeout=30
    )


@pytest.fixture
def sample_request():
    """Create a sample prompt request for testing."""
    return PromptRequest(
        prompt="What is the capital of France?",
        context={"user": "test_user", "session": "123"},
        temperature=0.5,
        max_tokens=100,
        system_message="You are a helpful assistant."
    )


@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI API response."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "Paris is the capital of France."
    mock_response.choices[0].finish_reason = "stop"
    mock_response.model = "gpt-3.5-turbo"
    mock_response.usage = Mock()
    mock_response.usage.prompt_tokens = 20
    mock_response.usage.completion_tokens = 8
    mock_response.usage.total_tokens = 28
    mock_response.id = "chatcmpl-test123"
    return mock_response


class TestOpenAIProviderInitialization:
    """Test OpenAI provider initialization and configuration validation."""
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_valid_initialization(self, valid_config):
        """Test successful provider initialization with valid config."""
        with patch('services.openai_provider.OpenAI') as mock_openai:
            provider = OpenAIProvider(valid_config)
            
            assert provider.config == valid_config
            assert provider.config.provider == AIProvider.OPENAI
            mock_openai.assert_called_once_with(
                api_key="test-api-key-12345",
                base_url=None,
                timeout=30
            )
    
    def test_initialization_without_openai_library(self, valid_config):
        """Test initialization fails when OpenAI library is not available."""
        with patch('services.openai_provider.OPENAI_AVAILABLE', False):
            with pytest.raises(AIProviderError) as exc_info:
                OpenAIProvider(valid_config)
            
            assert "OpenAI library not available" in str(exc_info.value)
            assert exc_info.value.error_code == "OPENAI_NOT_INSTALLED"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_invalid_provider_config(self, invalid_config):
        """Test initialization fails with wrong provider type."""
        with patch('services.openai_provider.OpenAI'):
            with pytest.raises(AIProviderError) as exc_info:
                OpenAIProvider(invalid_config)
            
            assert "Invalid provider" in str(exc_info.value)
            assert exc_info.value.error_code == "INVALID_PROVIDER"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_missing_api_key(self):
        """Test initialization fails with missing API key."""
        config = AIConfig(
            provider=AIProvider.OPENAI,
            api_key="",  # Empty API key
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        with patch('services.openai_provider.OpenAI'):
            with pytest.raises(AIProviderError) as exc_info:
                OpenAIProvider(config)
            
            assert "API key is required" in str(exc_info.value)
            assert exc_info.value.error_code == "MISSING_API_KEY"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_missing_model(self):
        """Test initialization fails with missing model."""
        # Pydantic will catch empty model during config creation
        with pytest.raises(Exception) as exc_info:
            AIConfig(
                provider=AIProvider.OPENAI,
                api_key="test-key",
                model="",  # Empty model
                temperature=0.7,
                max_tokens=500,
                timeout=30
            )
        
        assert "Model name is required" in str(exc_info.value)


class TestOpenAIProviderResponseGeneration:
    """Test OpenAI provider response generation functionality."""
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_successful_response_generation(self, valid_config, sample_request, mock_openai_response):
        """Test successful response generation."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_openai_response
            
            provider = OpenAIProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            # Verify response structure
            assert isinstance(response, AIResponse)
            assert response.success
            assert response.status == ResponseStatus.SUCCESS
            assert response.content == "Paris is the capital of France."
            assert response.provider == AIProvider.OPENAI
            assert response.model == "gpt-3.5-turbo"
            assert response.tokens_used == 28
            assert response.response_time is not None
            assert response.response_time > 0
            
            # Verify metadata
            assert response.metadata is not None
            assert response.metadata['model'] == "gpt-3.5-turbo"
            assert response.metadata['finish_reason'] == "stop"
            assert response.metadata['usage']['total_tokens'] == 28
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_message_preparation_with_system_message(self, valid_config, sample_request):
        """Test message preparation with explicit system message."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            provider = OpenAIProvider(valid_config)
            messages = provider._prepare_messages(sample_request)
            
            assert len(messages) == 2
            assert messages[0]['role'] == 'system'
            assert messages[0]['content'] == "You are a helpful assistant."
            assert messages[1]['role'] == 'user'
            assert messages[1]['content'] == "What is the capital of France?"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_message_preparation_with_context_only(self, valid_config):
        """Test message preparation with context but no system message."""
        request = PromptRequest(
            prompt="What is the capital of France?",
            context={"user": "test_user", "session": "123"}
        )
        
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            provider = OpenAIProvider(valid_config)
            messages = provider._prepare_messages(request)
            
            assert len(messages) == 2
            assert messages[0]['role'] == 'system'
            assert "Context information:" in messages[0]['content']
            assert "test_user" in messages[0]['content']
            assert messages[1]['role'] == 'user'
            assert messages[1]['content'] == "What is the capital of France?"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_message_preparation_without_context(self, valid_config):
        """Test message preparation without context or system message."""
        request = PromptRequest(prompt="What is the capital of France?")
        
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            provider = OpenAIProvider(valid_config)
            messages = provider._prepare_messages(request)
            
            assert len(messages) == 1
            assert messages[0]['role'] == 'user'
            assert messages[0]['content'] == "What is the capital of France?"


class TestOpenAIProviderErrorHandling:
    """Test OpenAI provider error handling functionality."""
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_authentication_error_handling(self, valid_config, sample_request):
        """Test handling of authentication errors."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Create a mock authentication error with proper class name
            class MockAuthenticationError(Exception):
                pass
            MockAuthenticationError.__name__ = "AuthenticationError"
            
            auth_error = MockAuthenticationError("Invalid API key")
            mock_client.chat.completions.create.side_effect = auth_error
            
            provider = OpenAIProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.ERROR
            assert "authentication failed" in response.error_message.lower()
            assert response.error_code == "AUTHENTICATION_ERROR"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_rate_limit_error_handling(self, valid_config, sample_request):
        """Test handling of rate limit errors."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Create a mock rate limit error with proper class name
            class MockRateLimitError(Exception):
                pass
            MockRateLimitError.__name__ = "RateLimitError"
            
            rate_error = MockRateLimitError("Rate limit exceeded")
            mock_client.chat.completions.create.side_effect = rate_error
            
            provider = OpenAIProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.RATE_LIMITED
            assert "rate limit exceeded" in response.error_message.lower()
            assert response.error_code == "RATE_LIMIT_ERROR"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_timeout_error_handling(self, valid_config, sample_request):
        """Test handling of timeout errors."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Create a mock timeout error with proper class name
            class MockTimeoutError(Exception):
                pass
            MockTimeoutError.__name__ = "TimeoutError"
            
            timeout_error = MockTimeoutError("Request timed out")
            mock_client.chat.completions.create.side_effect = timeout_error
            
            provider = OpenAIProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.TIMEOUT
            assert "timed out" in response.error_message.lower()
            assert response.error_code == "TIMEOUT_ERROR"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_invalid_request_error_handling(self, valid_config, sample_request):
        """Test handling of invalid request errors."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Create a mock bad request error with proper class name
            class MockBadRequestError(Exception):
                pass
            MockBadRequestError.__name__ = "BadRequestError"
            
            bad_request_error = MockBadRequestError("Invalid request")
            mock_client.chat.completions.create.side_effect = bad_request_error
            
            provider = OpenAIProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.INVALID_REQUEST
            assert "invalid request" in response.error_message.lower()
            assert response.error_code == "INVALID_REQUEST_ERROR"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_generic_error_handling(self, valid_config, sample_request):
        """Test handling of generic errors."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Create a generic error
            generic_error = Exception("Some unexpected error")
            mock_client.chat.completions.create.side_effect = generic_error
            
            provider = OpenAIProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.ERROR
            assert "API error" in response.error_message
            assert response.error_code == "API_ERROR"


class TestOpenAIProviderUtilityMethods:
    """Test OpenAI provider utility methods."""
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_validate_connection_success(self, valid_config):
        """Test successful connection validation."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Mock successful response
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message = Mock()
            mock_response.choices[0].message.content = "Hello"
            mock_response.choices[0].finish_reason = "stop"
            mock_response.model = "gpt-3.5-turbo"
            mock_response.usage = Mock()
            mock_response.usage.total_tokens = 5
            mock_client.chat.completions.create.return_value = mock_response
            
            provider = OpenAIProvider(valid_config)
            is_valid = provider.validate_connection()
            
            assert is_valid is True
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_validate_connection_failure(self, valid_config):
        """Test connection validation failure."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.side_effect = Exception("Connection failed")
            
            provider = OpenAIProvider(valid_config)
            is_valid = provider.validate_connection()
            
            assert is_valid is False
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_get_model_info(self, valid_config):
        """Test getting model information."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            provider = OpenAIProvider(valid_config)
            model_info = provider.get_model_info()
            
            assert model_info['provider'] == 'openai'
            assert model_info['model'] == 'gpt-3.5-turbo'
            assert model_info['temperature'] == 0.7
            assert model_info['max_tokens'] == 500
            assert model_info['timeout'] == 30
            assert model_info['supports_system_messages'] is True
            assert model_info['supports_context'] is True
            assert model_info['model_type'] == 'gpt-3.5'
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_model_type_detection(self, valid_config):
        """Test model type detection for different models."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Test GPT-4 model
            config_gpt4 = valid_config.model_copy()
            config_gpt4.model = "gpt-4"
            provider = OpenAIProvider(config_gpt4)
            assert provider._get_model_type() == 'gpt-4'
            
            # Test text completion model
            config_text = valid_config.model_copy()
            config_text.model = "text-davinci-003"
            provider = OpenAIProvider(config_text)
            assert provider._get_model_type() == 'completion'
            
            # Test legacy model
            config_legacy = valid_config.model_copy()
            config_legacy.model = "davinci"
            provider = OpenAIProvider(config_legacy)
            assert provider._get_model_type() == 'legacy'
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_context_formatting(self, valid_config):
        """Test context formatting functionality."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            provider = OpenAIProvider(valid_config)
            
            # Test normal dictionary formatting
            context = {"user": "test", "session": "123"}
            formatted = provider._format_context(context)
            assert "test" in formatted
            assert "123" in formatted
            
            # Test with complex nested data
            complex_context = {
                "user": {"name": "John", "age": 30},
                "preferences": ["option1", "option2"]
            }
            formatted = provider._format_context(complex_context)
            assert "John" in formatted
            assert "option1" in formatted


class TestOpenAIProviderStringRepresentation:
    """Test string representation methods."""
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_str_representation(self, valid_config):
        """Test __str__ method."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            provider = OpenAIProvider(valid_config)
            str_repr = str(provider)
            
            assert "OpenAIProvider" in str_repr
            assert "gpt-3.5-turbo" in str_repr
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_repr_representation(self, valid_config):
        """Test __repr__ method."""
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            provider = OpenAIProvider(valid_config)
            repr_str = repr(provider)
            
            assert "OpenAIProvider" in repr_str
            assert "gpt-3.5-turbo" in repr_str
            assert "temperature=0.7" in repr_str
            assert "max_tokens=500" in repr_str
            assert "timeout=30" in repr_str


if __name__ == "__main__":
    pytest.main([__file__])
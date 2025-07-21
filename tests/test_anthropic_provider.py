"""
Unit tests for Anthropic provider implementation.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import json

# Import the classes we're testing
from services.anthropic_provider import AnthropicProvider, ANTHROPIC_AVAILABLE
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
    """Create a valid Anthropic configuration for testing."""
    return AIConfig(
        provider=AIProvider.ANTHROPIC,
        api_key="test-api-key-12345",
        model="claude-3-haiku-20240307",
        temperature=0.7,
        max_tokens=500,
        timeout=30
    )


@pytest.fixture
def invalid_config():
    """Create an invalid configuration for testing."""
    return AIConfig(
        provider=AIProvider.OPENAI,  # Wrong provider
        api_key="test-api-key",
        model="gpt-3.5-turbo",
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
def mock_anthropic_response():
    """Create a mock Anthropic API response."""
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].text = "Paris is the capital of France."
    mock_response.stop_reason = "end_turn"
    mock_response.model = "claude-3-haiku-20240307"
    mock_response.usage = Mock()
    mock_response.usage.input_tokens = 20
    mock_response.usage.output_tokens = 8
    mock_response.id = "msg_test123"
    return mock_response


class TestAnthropicProviderInitialization:
    """Test Anthropic provider initialization and configuration validation."""
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_valid_initialization(self, valid_config):
        """Test successful provider initialization with valid config."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic:
            provider = AnthropicProvider(valid_config)
            
            assert provider.config == valid_config
            assert provider.config.provider == AIProvider.ANTHROPIC
            mock_anthropic.assert_called_once_with(
                api_key="test-api-key-12345",
                base_url=None,
                timeout=30
            )
    
    def test_initialization_without_anthropic_library(self, valid_config):
        """Test initialization fails when Anthropic library is not available."""
        with patch('services.anthropic_provider.ANTHROPIC_AVAILABLE', False):
            with pytest.raises(AIProviderError) as exc_info:
                AnthropicProvider(valid_config)
            
            assert "Anthropic library not available" in str(exc_info.value)
            assert exc_info.value.error_code == "ANTHROPIC_NOT_INSTALLED"
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_invalid_provider_config(self, invalid_config):
        """Test initialization fails with wrong provider type."""
        with patch('services.anthropic_provider.Anthropic'):
            with pytest.raises(AIProviderError) as exc_info:
                AnthropicProvider(invalid_config)
            
            assert "Invalid provider" in str(exc_info.value)
            assert exc_info.value.error_code == "INVALID_PROVIDER"
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_missing_api_key(self):
        """Test initialization fails with missing API key."""
        config = AIConfig(
            provider=AIProvider.ANTHROPIC,
            api_key="",  # Empty API key
            model="claude-3-haiku-20240307",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        with patch('services.anthropic_provider.Anthropic'):
            with pytest.raises(AIProviderError) as exc_info:
                AnthropicProvider(config)
            
            assert "API key is required" in str(exc_info.value)
            assert exc_info.value.error_code == "MISSING_API_KEY"
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_missing_model(self):
        """Test initialization fails with missing model."""
        # Pydantic will catch empty model during config creation
        with pytest.raises(Exception) as exc_info:
            AIConfig(
                provider=AIProvider.ANTHROPIC,
                api_key="test-key",
                model="",  # Empty model
                temperature=0.7,
                max_tokens=500,
                timeout=30
            )
        
        assert "Model name is required" in str(exc_info.value)


class TestAnthropicProviderResponseGeneration:
    """Test Anthropic provider response generation functionality."""
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_successful_response_generation(self, valid_config, sample_request, mock_anthropic_response):
        """Test successful response generation."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            mock_client.messages.create.return_value = mock_anthropic_response
            
            provider = AnthropicProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            # Verify response structure
            assert isinstance(response, AIResponse)
            assert response.success
            assert response.status == ResponseStatus.SUCCESS
            assert response.content == "Paris is the capital of France."
            assert response.provider == AIProvider.ANTHROPIC
            assert response.model == "claude-3-haiku-20240307"
            assert response.tokens_used == 28  # input_tokens + output_tokens
            assert response.response_time is not None
            assert response.response_time > 0
            
            # Verify metadata
            assert response.metadata is not None
            assert response.metadata['model'] == "claude-3-haiku-20240307"
            assert response.metadata['stop_reason'] == "end_turn"
            assert response.metadata['usage']['total_tokens'] == 28
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_message_preparation_with_system_message(self, valid_config, sample_request):
        """Test message preparation with explicit system message."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            provider = AnthropicProvider(valid_config)
            messages = provider._prepare_messages(sample_request)
            system_message = provider._prepare_system_message(sample_request)
            
            assert len(messages) == 1
            assert messages[0]['role'] == 'user'
            assert messages[0]['content'] == "What is the capital of France?"
            
            assert system_message == "You are a helpful assistant."
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_message_preparation_with_context_only(self, valid_config):
        """Test message preparation with context but no system message."""
        request = PromptRequest(
            prompt="What is the capital of France?",
            context={"user": "test_user", "session": "123"}
        )
        
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            provider = AnthropicProvider(valid_config)
            messages = provider._prepare_messages(request)
            system_message = provider._prepare_system_message(request)
            
            assert len(messages) == 1
            assert messages[0]['role'] == 'user'
            assert messages[0]['content'] == "What is the capital of France?"
            
            assert "Context information:" in system_message
            assert "test_user" in system_message
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_message_preparation_without_context(self, valid_config):
        """Test message preparation without context or system message."""
        request = PromptRequest(prompt="What is the capital of France?")
        
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            provider = AnthropicProvider(valid_config)
            messages = provider._prepare_messages(request)
            system_message = provider._prepare_system_message(request)
            
            assert len(messages) == 1
            assert messages[0]['role'] == 'user'
            assert messages[0]['content'] == "What is the capital of France?"
            
            assert system_message is None


class TestAnthropicProviderErrorHandling:
    """Test Anthropic provider error handling functionality."""
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_authentication_error_handling(self, valid_config, sample_request):
        """Test handling of authentication errors."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            # Create a mock authentication error
            auth_error = Exception("authentication failed")
            mock_client.messages.create.side_effect = auth_error
            
            provider = AnthropicProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.ERROR
            assert "authentication failed" in response.error_message.lower()
            assert response.error_code == "AUTHENTICATION_ERROR"
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_rate_limit_error_handling(self, valid_config, sample_request):
        """Test handling of rate limit errors."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            # Create a mock rate limit error
            rate_error = Exception("rate limit exceeded")
            mock_client.messages.create.side_effect = rate_error
            
            provider = AnthropicProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.RATE_LIMITED
            assert "rate limit exceeded" in response.error_message.lower()
            assert response.error_code == "RATE_LIMIT_ERROR"
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_timeout_error_handling(self, valid_config, sample_request):
        """Test handling of timeout errors."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            # Create a mock timeout error
            timeout_error = Exception("request timed out")
            mock_client.messages.create.side_effect = timeout_error
            
            provider = AnthropicProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.TIMEOUT
            assert "timed out" in response.error_message.lower()
            assert response.error_code == "TIMEOUT_ERROR"
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_invalid_request_error_handling(self, valid_config, sample_request):
        """Test handling of invalid request errors."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            # Create a mock bad request error
            bad_request_error = Exception("bad request")
            mock_client.messages.create.side_effect = bad_request_error
            
            provider = AnthropicProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.INVALID_REQUEST
            assert "invalid request" in response.error_message.lower()
            assert response.error_code == "INVALID_REQUEST_ERROR"
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_generic_error_handling(self, valid_config, sample_request):
        """Test handling of generic errors."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            # Create a generic error
            generic_error = Exception("Some unexpected error")
            mock_client.messages.create.side_effect = generic_error
            
            provider = AnthropicProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.ERROR
            assert "API error" in response.error_message
            assert response.error_code == "API_ERROR"


class TestAnthropicProviderUtilityMethods:
    """Test Anthropic provider utility methods."""
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_validate_connection_success(self, valid_config):
        """Test successful connection validation."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            # Mock successful response
            mock_response = Mock()
            mock_response.content = [Mock()]
            mock_response.content[0].text = "Hello"
            mock_response.stop_reason = "end_turn"
            mock_response.model = "claude-3-haiku-20240307"
            mock_response.usage = Mock()
            mock_response.usage.input_tokens = 2
            mock_response.usage.output_tokens = 3
            mock_client.messages.create.return_value = mock_response
            
            provider = AnthropicProvider(valid_config)
            is_valid = provider.validate_connection()
            
            assert is_valid is True
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_validate_connection_failure(self, valid_config):
        """Test connection validation failure."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            mock_client.messages.create.side_effect = Exception("Connection failed")
            
            provider = AnthropicProvider(valid_config)
            is_valid = provider.validate_connection()
            
            assert is_valid is False
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_get_model_info(self, valid_config):
        """Test getting model information."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            provider = AnthropicProvider(valid_config)
            model_info = provider.get_model_info()
            
            assert model_info['provider'] == 'anthropic'
            assert model_info['model'] == 'claude-3-haiku-20240307'
            assert model_info['temperature'] == 0.7
            assert model_info['max_tokens'] == 500
            assert model_info['timeout'] == 30
            assert model_info['supports_system_messages'] is True
            assert model_info['supports_context'] is True
            assert model_info['model_type'] == 'claude-3-haiku'
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_model_type_detection(self, valid_config):
        """Test model type detection for different models."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            # Test Claude 3 Opus model
            config_opus = valid_config.model_copy()
            config_opus.model = "claude-3-opus-20240229"
            provider = AnthropicProvider(config_opus)
            assert provider._get_model_type() == 'claude-3-opus'
            
            # Test Claude 3 Sonnet model
            config_sonnet = valid_config.model_copy()
            config_sonnet.model = "claude-3-sonnet-20240229"
            provider = AnthropicProvider(config_sonnet)
            assert provider._get_model_type() == 'claude-3-sonnet'
            
            # Test Claude 2 model
            config_claude2 = valid_config.model_copy()
            config_claude2.model = "claude-2.1"
            provider = AnthropicProvider(config_claude2)
            assert provider._get_model_type() == 'claude-2'
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_context_formatting(self, valid_config):
        """Test context formatting functionality."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            provider = AnthropicProvider(valid_config)
            
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


class TestAnthropicProviderStringRepresentation:
    """Test string representation methods."""
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_str_representation(self, valid_config):
        """Test __str__ method."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            provider = AnthropicProvider(valid_config)
            str_repr = str(provider)
            
            assert "AnthropicProvider" in str_repr
            assert "claude-3-haiku-20240307" in str_repr
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_repr_representation(self, valid_config):
        """Test __repr__ method."""
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            
            provider = AnthropicProvider(valid_config)
            repr_str = repr(provider)
            
            assert "AnthropicProvider" in repr_str
            assert "claude-3-haiku-20240307" in repr_str
            assert "temperature=0.7" in repr_str
            assert "max_tokens=500" in repr_str
            assert "timeout=30" in repr_str


if __name__ == "__main__":
    pytest.main([__file__])
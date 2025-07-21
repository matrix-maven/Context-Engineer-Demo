"""
Unit tests for OpenRouter provider implementation.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import json

# Import the classes we're testing
from services.openrouter_provider import OpenRouterProvider, REQUESTS_AVAILABLE
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
    """Create a valid OpenRouter configuration for testing."""
    return AIConfig(
        provider=AIProvider.OPENROUTER,
        api_key="sk-or-test-key-12345",
        model="openai/gpt-3.5-turbo",
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
def mock_openrouter_response():
    """Create a mock OpenRouter API response."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "model": "openai/gpt-3.5-turbo",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Paris is the capital of France."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 8,
            "total_tokens": 28
        },
        "provider": {
            "name": "OpenAI"
        }
    }
    return mock_response


class TestOpenRouterProviderInitialization:
    """Test OpenRouter provider initialization and configuration validation."""
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_valid_initialization(self, valid_config):
        """Test successful provider initialization with valid config."""
        provider = OpenRouterProvider(valid_config)
        
        assert provider.config == valid_config
        assert provider.config.provider == AIProvider.OPENROUTER
        assert provider.config.base_url == "https://openrouter.ai/api/v1"
    
    def test_initialization_without_requests_library(self, valid_config):
        """Test initialization fails when requests library is not available."""
        with patch('services.openrouter_provider.REQUESTS_AVAILABLE', False):
            with pytest.raises(AIProviderError) as exc_info:
                OpenRouterProvider(valid_config)
            
            assert "Requests library not available" in str(exc_info.value)
            assert exc_info.value.error_code == "REQUESTS_NOT_INSTALLED"
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_missing_api_key(self):
        """Test initialization fails with missing API key."""
        config = AIConfig(
            provider=AIProvider.OPENROUTER,
            api_key="",  # Empty API key
            model="openai/gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        with pytest.raises(AIProviderError) as exc_info:
            OpenRouterProvider(config)
        
        assert "API key is required" in str(exc_info.value)
        assert exc_info.value.error_code == "MISSING_API_KEY"


class TestOpenRouterProviderResponseGeneration:
    """Test OpenRouter provider response generation functionality."""
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_successful_response_generation(self, valid_config, sample_request, mock_openrouter_response):
        """Test successful response generation."""
        with patch('services.openrouter_provider.requests') as mock_requests:
            mock_requests.post.return_value = mock_openrouter_response
            
            provider = OpenRouterProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            # Verify response structure
            assert isinstance(response, AIResponse)
            assert response.success
            assert response.status == ResponseStatus.SUCCESS
            assert response.content == "Paris is the capital of France."
            assert response.provider == AIProvider.OPENROUTER
            assert response.model == "openai/gpt-3.5-turbo"
            assert response.tokens_used == 28
            assert response.response_time is not None
            assert response.response_time > 0
            
            # Verify metadata
            assert response.metadata is not None
            assert response.metadata['model'] == "openai/gpt-3.5-turbo"
            assert response.metadata['finish_reason'] == "stop"
            assert response.metadata['usage']['total_tokens'] == 28
            assert response.metadata['provider_used'] == "OpenAI"
            
            # Verify API call was made correctly
            mock_requests.post.assert_called_once()
            call_args = mock_requests.post.call_args
            
            assert call_args[1]['json']['model'] == 'openai/gpt-3.5-turbo'
            assert call_args[1]['json']['temperature'] == 0.5
            assert call_args[1]['json']['max_tokens'] == 100
            assert len(call_args[1]['json']['messages']) == 2  # System + user message
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_message_preparation_with_system_message(self, valid_config, sample_request):
        """Test message preparation with explicit system message."""
        provider = OpenRouterProvider(valid_config)
        messages = provider._prepare_messages(sample_request)
        
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert messages[0]['content'] == "You are a helpful assistant."
        assert messages[1]['role'] == 'user'
        assert messages[1]['content'] == "What is the capital of France?"
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_message_preparation_with_context_only(self, valid_config):
        """Test message preparation with context but no system message."""
        request = PromptRequest(
            prompt="What is the capital of France?",
            context={"user": "test_user", "session": "123"}
        )
        
        provider = OpenRouterProvider(valid_config)
        messages = provider._prepare_messages(request)
        
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert "Context information:" in messages[0]['content']
        assert "test_user" in messages[0]['content']
        assert messages[1]['role'] == 'user'
        assert messages[1]['content'] == "What is the capital of France?"


class TestOpenRouterProviderErrorHandling:
    """Test OpenRouter provider error handling functionality."""
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_authentication_error_handling(self, valid_config, sample_request):
        """Test handling of authentication errors."""
        with patch('services.openrouter_provider.requests') as mock_requests:
            # Create a mock HTTP 401 error
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = {
                "error": {"message": "Invalid API key"}
            }
            
            mock_error = Exception("401 Client Error")
            mock_error.response = mock_response
            mock_requests.post.side_effect = mock_error
            
            provider = OpenRouterProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.ERROR
            assert "authentication failed" in response.error_message.lower()
            assert response.error_code == "AUTHENTICATION_ERROR"
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_rate_limit_error_handling(self, valid_config, sample_request):
        """Test handling of rate limit errors."""
        with patch('services.openrouter_provider.requests') as mock_requests:
            # Create a mock HTTP 429 error
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.json.return_value = {
                "error": {"message": "Rate limit exceeded"}
            }
            
            mock_error = Exception("429 Too Many Requests")
            mock_error.response = mock_response
            mock_requests.post.side_effect = mock_error
            
            provider = OpenRouterProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.RATE_LIMITED
            assert "rate limit exceeded" in response.error_message.lower()
            assert response.error_code == "RATE_LIMIT_ERROR"
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_timeout_error_handling(self, valid_config, sample_request):
        """Test handling of timeout errors."""
        with patch('services.openrouter_provider.requests') as mock_requests:
            timeout_error = Exception("Request timed out")
            mock_requests.post.side_effect = timeout_error
            
            provider = OpenRouterProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.TIMEOUT
            assert "timed out" in response.error_message.lower()
            assert response.error_code == "TIMEOUT_ERROR"
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_invalid_json_response_handling(self, valid_config, sample_request):
        """Test handling of invalid JSON responses."""
        with patch('services.openrouter_provider.requests') as mock_requests:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_response.text = "Invalid response"
            mock_requests.post.return_value = mock_response
            
            provider = OpenRouterProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.ERROR
            assert "Invalid JSON response" in response.error_message
            assert response.error_code == "INVALID_RESPONSE"


class TestOpenRouterProviderUtilityMethods:
    """Test OpenRouter provider utility methods."""
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_get_model_info(self, valid_config):
        """Test getting model information."""
        provider = OpenRouterProvider(valid_config)
        model_info = provider.get_model_info()
        
        assert model_info['provider'] == 'openrouter'
        assert model_info['model'] == 'openai/gpt-3.5-turbo'
        assert model_info['temperature'] == 0.7
        assert model_info['max_tokens'] == 500
        assert model_info['timeout'] == 30
        assert model_info['base_url'] == "https://openrouter.ai/api/v1"
        assert model_info['supports_system_messages'] is True
        assert model_info['supports_context'] is True
        assert model_info['model_type'] == 'openai-gpt-3.5'
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_model_type_detection(self, valid_config):
        """Test model type detection for different models."""
        # Test OpenAI GPT-4
        config_gpt4 = valid_config.model_copy()
        config_gpt4.model = "openai/gpt-4"
        provider = OpenRouterProvider(config_gpt4)
        assert provider._get_model_type() == 'openai-gpt-4'
        
        # Test Anthropic Claude
        config_claude = valid_config.model_copy()
        config_claude.model = "anthropic/claude-3-haiku"
        provider = OpenRouterProvider(config_claude)
        assert provider._get_model_type() == 'anthropic-claude'
        
        # Test Google Gemini
        config_gemini = valid_config.model_copy()
        config_gemini.model = "google/gemini-1.5-flash"
        provider = OpenRouterProvider(config_gemini)
        assert provider._get_model_type() == 'google-gemini'
        
        # Test Meta Llama
        config_llama = valid_config.model_copy()
        config_llama.model = "meta/llama-2-70b"
        provider = OpenRouterProvider(config_llama)
        assert provider._get_model_type() == 'meta-llama'
    
    @pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="Requests library not available")
    def test_context_formatting(self, valid_config):
        """Test context formatting functionality."""
        provider = OpenRouterProvider(valid_config)
        
        # Test normal dictionary formatting
        context = {"user": "test", "session": "123"}
        formatted = provider._format_context(context)
        assert "test" in formatted
        assert "123" in formatted


if __name__ == "__main__":
    pytest.main([__file__])
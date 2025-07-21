"""
Unit tests for Gemini provider implementation.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import json

# Import the classes we're testing
from services.gemini_provider import GeminiProvider, GEMINI_AVAILABLE
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
    """Create a valid Gemini configuration for testing."""
    return AIConfig(
        provider=AIProvider.GEMINI,
        api_key="AIza-test-key-12345",
        model="gemini-1.5-flash",
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
def mock_gemini_response():
    """Create a mock Gemini API response."""
    mock_response = Mock()
    mock_response.text = "Paris is the capital of France."
    mock_response.candidates = [Mock()]
    mock_response.candidates[0].content = Mock()
    mock_response.candidates[0].content.parts = [Mock()]
    mock_response.candidates[0].content.parts[0].text = "Paris is the capital of France."
    mock_response.candidates[0].finish_reason = "STOP"
    mock_response.usage_metadata = Mock()
    mock_response.usage_metadata.prompt_token_count = 20
    mock_response.usage_metadata.candidates_token_count = 8
    return mock_response


class TestGeminiProviderInitialization:
    """Test Gemini provider initialization and configuration validation."""
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_valid_initialization(self, valid_config):
        """Test successful provider initialization with valid config."""
        with patch('services.gemini_provider.genai') as mock_genai:
            mock_model = Mock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            provider = GeminiProvider(valid_config)
            
            assert provider.config == valid_config
            assert provider.config.provider == AIProvider.GEMINI
            mock_genai.configure.assert_called_once_with(api_key="AIza-test-key-12345")
            mock_genai.GenerativeModel.assert_called_once_with("gemini-1.5-flash")
    
    def test_initialization_without_gemini_library(self, valid_config):
        """Test initialization fails when Gemini library is not available."""
        with patch('services.gemini_provider.GEMINI_AVAILABLE', False):
            with pytest.raises(AIProviderError) as exc_info:
                GeminiProvider(valid_config)
            
            assert "Google Gemini library not available" in str(exc_info.value)
            assert exc_info.value.error_code == "GEMINI_NOT_INSTALLED"
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_missing_api_key(self):
        """Test initialization fails with missing API key."""
        config = AIConfig(
            provider=AIProvider.GEMINI,
            api_key="",  # Empty API key
            model="gemini-1.5-flash",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        with patch('services.gemini_provider.genai'):
            with pytest.raises(AIProviderError) as exc_info:
                GeminiProvider(config)
            
            assert "API key is required" in str(exc_info.value)
            assert exc_info.value.error_code == "MISSING_API_KEY"


class TestGeminiProviderResponseGeneration:
    """Test Gemini provider response generation functionality."""
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_successful_response_generation(self, valid_config, sample_request, mock_gemini_response):
        """Test successful response generation."""
        with patch('services.gemini_provider.genai') as mock_genai:
            mock_model = Mock()
            mock_genai.GenerativeModel.return_value = mock_model
            mock_model.generate_content.return_value = mock_gemini_response
            
            provider = GeminiProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            # Verify response structure
            assert isinstance(response, AIResponse)
            assert response.success
            assert response.status == ResponseStatus.SUCCESS
            assert response.content == "Paris is the capital of France."
            assert response.provider == AIProvider.GEMINI
            assert response.model == "gemini-1.5-flash"
            assert response.tokens_used == 28  # prompt + candidates tokens
            assert response.response_time is not None
            assert response.response_time > 0
            
            # Verify metadata
            assert response.metadata is not None
            assert response.metadata['model'] == "gemini-1.5-flash"
            assert response.metadata['finish_reason'] == "STOP"
            assert response.metadata['usage']['total_tokens'] == 28
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_prompt_preparation(self, valid_config, sample_request):
        """Test prompt preparation with system message and context."""
        with patch('services.gemini_provider.genai') as mock_genai:
            mock_model = Mock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            provider = GeminiProvider(valid_config)
            prompt = provider._prepare_prompt(sample_request)
            
            assert "System: You are a helpful assistant." in prompt
            assert "Context:" in prompt
            assert "test_user" in prompt
            assert "User: What is the capital of France?" in prompt


class TestGeminiProviderErrorHandling:
    """Test Gemini provider error handling functionality."""
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_authentication_error_handling(self, valid_config, sample_request):
        """Test handling of authentication errors."""
        with patch('services.gemini_provider.genai') as mock_genai:
            mock_model = Mock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            auth_error = Exception("API key invalid")
            mock_model.generate_content.side_effect = auth_error
            
            provider = GeminiProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.ERROR
            assert "authentication failed" in response.error_message.lower()
            assert response.error_code == "AUTHENTICATION_ERROR"
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_quota_error_handling(self, valid_config, sample_request):
        """Test handling of quota/rate limit errors."""
        with patch('services.gemini_provider.genai') as mock_genai:
            mock_model = Mock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            quota_error = Exception("quota exceeded")
            mock_model.generate_content.side_effect = quota_error
            
            provider = GeminiProvider(valid_config)
            response = provider.generate_response(sample_request)
            
            assert not response.success
            assert response.status == ResponseStatus.RATE_LIMITED
            assert "rate limit exceeded" in response.error_message.lower()
            assert response.error_code == "RATE_LIMIT_ERROR"


class TestGeminiProviderUtilityMethods:
    """Test Gemini provider utility methods."""
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_get_model_info(self, valid_config):
        """Test getting model information."""
        with patch('services.gemini_provider.genai') as mock_genai:
            mock_model = Mock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            provider = GeminiProvider(valid_config)
            model_info = provider.get_model_info()
            
            assert model_info['provider'] == 'gemini'
            assert model_info['model'] == 'gemini-1.5-flash'
            assert model_info['temperature'] == 0.7
            assert model_info['max_tokens'] == 500
            assert model_info['timeout'] == 30
            assert model_info['supports_system_messages'] is True
            assert model_info['supports_context'] is True
            assert model_info['model_type'] == 'gemini-1.5-flash'
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_model_type_detection(self, valid_config):
        """Test model type detection for different models."""
        with patch('services.gemini_provider.genai') as mock_genai:
            mock_model = Mock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            # Test Gemini 1.5 Flash
            provider = GeminiProvider(valid_config)
            assert provider._get_model_type() == 'gemini-1.5-flash'
            
            # Test Gemini Ultra
            config_ultra = valid_config.model_copy()
            config_ultra.model = "gemini-ultra"
            provider = GeminiProvider(config_ultra)
            assert provider._get_model_type() == 'gemini-ultra'
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="Gemini library not available")
    def test_context_formatting(self, valid_config):
        """Test context formatting functionality."""
        with patch('services.gemini_provider.genai') as mock_genai:
            mock_model = Mock()
            mock_genai.GenerativeModel.return_value = mock_model
            
            provider = GeminiProvider(valid_config)
            
            # Test normal dictionary formatting
            context = {"user": "test", "session": "123"}
            formatted = provider._format_context(context)
            assert "test" in formatted
            assert "123" in formatted


if __name__ == "__main__":
    pytest.main([__file__])
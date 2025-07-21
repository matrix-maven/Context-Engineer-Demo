"""
Unit tests for AI Service Orchestrator.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import time

# Import the classes we're testing
from services.ai_orchestrator import AIServiceOrchestrator
from services.ai_service import (
    AIResponse, PromptRequest, ResponseStatus,
    AIProviderError, AIProviderTimeoutError, AIProviderRateLimitError,
    AIProviderAuthenticationError, AIProviderInvalidRequestError
)
from config.ai_config import AIConfig
from config.settings import AIProvider


# Test fixtures
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
def mock_successful_response():
    """Create a mock successful AI response."""
    return AIResponse(
        content="Paris is the capital of France.",
        provider=AIProvider.OPENAI,
        model="gpt-3.5-turbo",
        status=ResponseStatus.SUCCESS,
        tokens_used=28,
        response_time=1.5
    )


@pytest.fixture
def mock_error_response():
    """Create a mock error AI response."""
    return AIResponse(
        content="",
        provider=AIProvider.OPENAI,
        model="gpt-3.5-turbo",
        status=ResponseStatus.ERROR,
        error_message="API error occurred",
        error_code="API_ERROR"
    )


class TestAIServiceOrchestratorInitialization:
    """Test AI Service Orchestrator initialization."""
    
    def test_initialization_with_no_providers(self):
        """Test initialization when no providers are available."""
        with patch('services.ai_orchestrator.get_available_providers', return_value=[]):
            orchestrator = AIServiceOrchestrator()
            
            assert len(orchestrator.providers) == 0
            assert orchestrator.current_provider is None
            assert orchestrator.enable_caching is True
            assert orchestrator.fallback_enabled is True
    
    def test_initialization_with_mock_providers(self):
        """Test initialization with mock providers."""
        with patch('services.ai_orchestrator.get_available_providers', return_value=[AIProvider.OPENAI]):
            with patch('services.ai_orchestrator.load_ai_config') as mock_load_config:
                with patch('services.ai_orchestrator.OpenAIProvider') as mock_provider_class:
                    # Setup mocks
                    mock_config = Mock()
                    mock_load_config.return_value = mock_config
                    mock_provider = Mock()
                    mock_provider_class.return_value = mock_provider
                    
                    orchestrator = AIServiceOrchestrator()
                    
                    assert AIProvider.OPENAI in orchestrator.providers
                    assert orchestrator.current_provider == AIProvider.OPENAI
                    assert AIProvider.OPENAI in orchestrator.provider_stats
    
    def test_initialization_with_default_provider(self):
        """Test initialization with specified default provider."""
        with patch('services.ai_orchestrator.get_available_providers', return_value=[AIProvider.OPENAI, AIProvider.ANTHROPIC]):
            with patch('services.ai_orchestrator.load_ai_config') as mock_load_config:
                with patch('services.ai_orchestrator.OpenAIProvider') as mock_openai:
                    with patch('services.ai_orchestrator.AnthropicProvider') as mock_anthropic:
                        with patch('services.ai_orchestrator.OPENAI_AVAILABLE', True):
                            with patch('services.ai_orchestrator.ANTHROPIC_AVAILABLE', True):
                                mock_config = Mock()
                                mock_load_config.return_value = mock_config
                                mock_openai.return_value = Mock()
                                mock_anthropic.return_value = Mock()
                                
                                orchestrator = AIServiceOrchestrator(default_provider=AIProvider.ANTHROPIC)
                                
                                assert orchestrator.current_provider == AIProvider.ANTHROPIC


class TestAIServiceOrchestratorProviderManagement:
    """Test provider management functionality."""
    
    def test_set_provider_success(self):
        """Test successful provider switching."""
        orchestrator = AIServiceOrchestrator()
        
        # Mock a provider
        mock_provider = Mock()
        orchestrator.providers[AIProvider.OPENAI] = mock_provider
        
        result = orchestrator.set_provider(AIProvider.OPENAI)
        
        assert result is True
        assert orchestrator.current_provider == AIProvider.OPENAI
    
    def test_set_provider_unavailable(self):
        """Test setting an unavailable provider."""
        orchestrator = AIServiceOrchestrator()
        
        result = orchestrator.set_provider(AIProvider.OPENAI)
        
        assert result is False
        assert orchestrator.current_provider is None
    
    def test_get_available_providers(self):
        """Test getting list of available providers."""
        orchestrator = AIServiceOrchestrator()
        
        # Mock providers
        mock_provider1 = Mock()
        mock_provider2 = Mock()
        orchestrator.providers[AIProvider.OPENAI] = mock_provider1
        orchestrator.providers[AIProvider.ANTHROPIC] = mock_provider2
        
        available = orchestrator.get_available_providers()
        
        assert AIProvider.OPENAI in available
        assert AIProvider.ANTHROPIC in available
        assert len(available) == 2


class TestAIServiceOrchestratorResponseGeneration:
    """Test response generation functionality."""
    
    def test_generate_response_success(self, sample_request, mock_successful_response):
        """Test successful response generation."""
        orchestrator = AIServiceOrchestrator(enable_caching=False)
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.generate_response.return_value = mock_successful_response
        orchestrator.providers[AIProvider.OPENAI] = mock_provider
        orchestrator.current_provider = AIProvider.OPENAI
        orchestrator.provider_stats[AIProvider.OPENAI] = {
            'requests': 0, 'successes': 0, 'failures': 0,
            'total_response_time': 0.0, 'average_response_time': 0.0,
            'last_used': None, 'consecutive_failures': 0
        }
        
        response = orchestrator.generate_response(sample_request)
        
        assert response.success
        assert response.content == "Paris is the capital of France."
        mock_provider.generate_response.assert_called_once_with(sample_request)
        
        # Check stats were updated
        stats = orchestrator.provider_stats[AIProvider.OPENAI]
        assert stats['requests'] == 1
        assert stats['successes'] == 1
        assert stats['failures'] == 0
    
    def test_generate_response_no_provider(self, sample_request):
        """Test response generation with no provider available."""
        orchestrator = AIServiceOrchestrator()
        
        response = orchestrator.generate_response(sample_request)
        
        assert not response.success
        assert response.status == ResponseStatus.ERROR
        assert "No AI provider available" in response.error_message
    
    def test_generate_response_with_specific_provider(self, sample_request, mock_successful_response):
        """Test response generation with specific provider."""
        orchestrator = AIServiceOrchestrator(enable_caching=False)
        
        # Mock providers
        mock_openai = Mock()
        mock_anthropic = Mock()
        mock_anthropic.generate_response.return_value = mock_successful_response
        
        orchestrator.providers[AIProvider.OPENAI] = mock_openai
        orchestrator.providers[AIProvider.ANTHROPIC] = mock_anthropic
        orchestrator.current_provider = AIProvider.OPENAI
        orchestrator.provider_stats[AIProvider.ANTHROPIC] = {
            'requests': 0, 'successes': 0, 'failures': 0,
            'total_response_time': 0.0, 'average_response_time': 0.0,
            'last_used': None, 'consecutive_failures': 0
        }
        
        response = orchestrator.generate_response(sample_request, provider=AIProvider.ANTHROPIC)
        
        assert response.success
        mock_anthropic.generate_response.assert_called_once_with(sample_request)
        mock_openai.generate_response.assert_not_called()


class TestAIServiceOrchestratorCaching:
    """Test response caching functionality."""
    
    def test_cache_response_and_retrieval(self, sample_request, mock_successful_response):
        """Test caching and retrieving responses."""
        orchestrator = AIServiceOrchestrator(enable_caching=True, cache_ttl_seconds=300)
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.generate_response.return_value = mock_successful_response
        orchestrator.providers[AIProvider.OPENAI] = mock_provider
        orchestrator.current_provider = AIProvider.OPENAI
        orchestrator.provider_stats[AIProvider.OPENAI] = {
            'requests': 0, 'successes': 0, 'failures': 0,
            'total_response_time': 0.0, 'average_response_time': 0.0,
            'last_used': None, 'consecutive_failures': 0
        }
        
        # First request - should call provider
        response1 = orchestrator.generate_response(sample_request)
        assert response1.success
        assert mock_provider.generate_response.call_count == 1
        
        # Second identical request - should use cache
        response2 = orchestrator.generate_response(sample_request)
        assert response2.success
        assert response2.content == response1.content
        assert mock_provider.generate_response.call_count == 1  # No additional call
    
    def test_cache_expiration(self, sample_request, mock_successful_response):
        """Test cache expiration."""
        orchestrator = AIServiceOrchestrator(enable_caching=True, cache_ttl_seconds=1)
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.generate_response.return_value = mock_successful_response
        orchestrator.providers[AIProvider.OPENAI] = mock_provider
        orchestrator.current_provider = AIProvider.OPENAI
        orchestrator.provider_stats[AIProvider.OPENAI] = {
            'requests': 0, 'successes': 0, 'failures': 0,
            'total_response_time': 0.0, 'average_response_time': 0.0,
            'last_used': None, 'consecutive_failures': 0
        }
        
        # First request
        response1 = orchestrator.generate_response(sample_request)
        assert response1.success
        assert mock_provider.generate_response.call_count == 1
        
        # Wait for cache to expire
        time.sleep(1.1)
        
        # Second request - should call provider again
        response2 = orchestrator.generate_response(sample_request)
        assert response2.success
        assert mock_provider.generate_response.call_count == 2
    
    def test_cache_disabled(self, sample_request, mock_successful_response):
        """Test behavior when caching is disabled."""
        orchestrator = AIServiceOrchestrator(enable_caching=False)
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.generate_response.return_value = mock_successful_response
        orchestrator.providers[AIProvider.OPENAI] = mock_provider
        orchestrator.current_provider = AIProvider.OPENAI
        orchestrator.provider_stats[AIProvider.OPENAI] = {
            'requests': 0, 'successes': 0, 'failures': 0,
            'total_response_time': 0.0, 'average_response_time': 0.0,
            'last_used': None, 'consecutive_failures': 0
        }
        
        # Two identical requests - should call provider both times
        response1 = orchestrator.generate_response(sample_request)
        response2 = orchestrator.generate_response(sample_request)
        
        assert response1.success
        assert response2.success
        assert mock_provider.generate_response.call_count == 2


class TestAIServiceOrchestratorFallback:
    """Test fallback functionality."""
    
    def test_fallback_on_provider_failure(self, sample_request, mock_successful_response, mock_error_response):
        """Test fallback to another provider on failure."""
        orchestrator = AIServiceOrchestrator(enable_caching=False, fallback_enabled=True, max_retries=0)
        
        # Mock providers
        mock_openai = Mock()
        mock_anthropic = Mock()
        mock_openai.generate_response.return_value = mock_error_response
        mock_anthropic.generate_response.return_value = mock_successful_response
        
        orchestrator.providers[AIProvider.OPENAI] = mock_openai
        orchestrator.providers[AIProvider.ANTHROPIC] = mock_anthropic
        orchestrator.current_provider = AIProvider.OPENAI
        
        # Initialize stats
        for provider in [AIProvider.OPENAI, AIProvider.ANTHROPIC]:
            orchestrator.provider_stats[provider] = {
                'requests': 0, 'successes': 0, 'failures': 0,
                'total_response_time': 0.0, 'average_response_time': 0.0,
                'last_used': None, 'consecutive_failures': 0
            }
        
        response = orchestrator.generate_response(sample_request)
        
        assert response.success
        assert response.content == "Paris is the capital of France."
        mock_openai.generate_response.assert_called_once()
        mock_anthropic.generate_response.assert_called_once()
    
    def test_fallback_disabled(self, sample_request, mock_error_response):
        """Test behavior when fallback is disabled."""
        orchestrator = AIServiceOrchestrator(enable_caching=False, fallback_enabled=False, max_retries=0)
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.generate_response.return_value = mock_error_response
        orchestrator.providers[AIProvider.OPENAI] = mock_provider
        orchestrator.current_provider = AIProvider.OPENAI
        orchestrator.provider_stats[AIProvider.OPENAI] = {
            'requests': 0, 'successes': 0, 'failures': 0,
            'total_response_time': 0.0, 'average_response_time': 0.0,
            'last_used': None, 'consecutive_failures': 0
        }
        
        response = orchestrator.generate_response(sample_request)
        
        assert not response.success
        assert response.status == ResponseStatus.ERROR
        mock_provider.generate_response.assert_called_once()


class TestAIServiceOrchestratorUtilityMethods:
    """Test utility methods."""
    
    def test_get_provider_stats(self):
        """Test getting provider statistics."""
        orchestrator = AIServiceOrchestrator()
        
        # Mock stats
        orchestrator.provider_stats[AIProvider.OPENAI] = {
            'requests': 10,
            'successes': 8,
            'failures': 2,
            'total_response_time': 15.0,
            'average_response_time': 1.5,
            'last_used': datetime.now(),
            'consecutive_failures': 0
        }
        
        stats = orchestrator.get_provider_stats()
        
        assert 'openai' in stats
        assert stats['openai']['requests'] == 10
        assert stats['openai']['success_rate'] == 0.8
        assert 'last_used' in stats['openai']
    
    def test_get_provider_info(self):
        """Test getting provider information."""
        orchestrator = AIServiceOrchestrator()
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.get_model_info.return_value = {
            'provider': 'openai',
            'model': 'gpt-3.5-turbo',
            'temperature': 0.7
        }
        orchestrator.providers[AIProvider.OPENAI] = mock_provider
        orchestrator.current_provider = AIProvider.OPENAI
        orchestrator.provider_stats[AIProvider.OPENAI] = {}
        
        info = orchestrator.get_provider_info()
        
        assert info['provider'] == 'openai'
        assert info['model'] == 'gpt-3.5-turbo'
        assert 'orchestrator_stats' in info
        assert info['is_current_provider'] is True
    
    def test_validate_provider_connection(self):
        """Test provider connection validation."""
        orchestrator = AIServiceOrchestrator()
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.validate_connection.return_value = True
        orchestrator.providers[AIProvider.OPENAI] = mock_provider
        orchestrator.current_provider = AIProvider.OPENAI
        
        result = orchestrator.validate_provider_connection()
        
        assert result is True
        mock_provider.validate_connection.assert_called_once()
    
    def test_clear_cache(self):
        """Test cache clearing."""
        orchestrator = AIServiceOrchestrator()
        
        # Add some cache entries
        orchestrator.response_cache['key1'] = {'data': 'value1'}
        orchestrator.response_cache['key2'] = {'data': 'value2'}
        
        assert len(orchestrator.response_cache) == 2
        
        orchestrator.clear_cache()
        
        assert len(orchestrator.response_cache) == 0
    
    def test_get_cache_stats(self):
        """Test getting cache statistics."""
        orchestrator = AIServiceOrchestrator(cache_ttl_seconds=300)
        
        # Add cache entries
        current_time = datetime.now().timestamp()
        orchestrator.response_cache['valid'] = {'timestamp': current_time}
        orchestrator.response_cache['expired'] = {'timestamp': current_time - 400}
        
        stats = orchestrator.get_cache_stats()
        
        assert stats['total_entries'] == 2
        assert stats['valid_entries'] == 1
        assert stats['expired_entries'] == 1
        assert stats['cache_ttl_seconds'] == 300
        assert stats['cache_enabled'] is True


if __name__ == "__main__":
    pytest.main([__file__])
"""
Integration tests for Anthropic provider with AI service infrastructure.
"""
import pytest
from unittest.mock import Mock, patch
import os

from services.anthropic_provider import AnthropicProvider, ANTHROPIC_AVAILABLE
from services.ai_service import PromptRequest, ResponseStatus
from config.ai_config import AIConfig, load_ai_config
from config.settings import AIProvider


class TestAnthropicProviderIntegration:
    """Test Anthropic provider integration with the broader AI service infrastructure."""
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_provider_creation_from_config(self):
        """Test creating Anthropic provider from configuration."""
        config = AIConfig(
            provider=AIProvider.ANTHROPIC,
            api_key="test-api-key-12345",
            model="claude-3-haiku-20240307",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic:
            provider = AnthropicProvider(config)
            
            assert provider.config == config
            assert isinstance(provider, AnthropicProvider)
            mock_anthropic.assert_called_once()
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_provider_with_environment_config(self):
        """Test creating Anthropic provider from environment configuration."""
        # Mock environment variables
        with patch.dict(os.environ, {
            'ANTHROPIC_API_KEY': 'test-env-key',
            'ANTHROPIC_MODEL': 'claude-3-opus-20240229',
            'AI_TEMPERATURE': '0.5',
            'AI_MAX_TOKENS': '1000'
        }):
            config = load_ai_config(AIProvider.ANTHROPIC)
            
            assert config is not None
            assert config.provider == AIProvider.ANTHROPIC
            assert config.get_api_key() == 'test-env-key'
            assert config.model == 'claude-3-opus-20240229'
            assert config.temperature == 0.5
            assert config.max_tokens == 1000
            
            with patch('services.anthropic_provider.Anthropic') as mock_anthropic:
                provider = AnthropicProvider(config)
                assert provider.config.model == 'claude-3-opus-20240229'
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_end_to_end_request_flow(self):
        """Test complete request flow from prompt to response."""
        config = AIConfig(
            provider=AIProvider.ANTHROPIC,
            api_key="test-api-key",
            model="claude-3-haiku-20240307",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        # Create mock Anthropic response
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "This is a test response from Claude."
        mock_response.stop_reason = "end_turn"
        mock_response.model = "claude-3-haiku-20240307"
        mock_response.usage = Mock()
        mock_response.usage.input_tokens = 15
        mock_response.usage.output_tokens = 10
        mock_response.id = "msg_test123"
        
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            mock_client.messages.create.return_value = mock_response
            
            # Create provider and make request
            provider = AnthropicProvider(config)
            
            request = PromptRequest(
                prompt="What is artificial intelligence?",
                context={"topic": "AI", "level": "beginner"},
                temperature=0.5,
                max_tokens=100,
                system_message="You are a helpful AI assistant."
            )
            
            response = provider.generate_response(request)
            
            # Verify response
            assert response.success
            assert response.status == ResponseStatus.SUCCESS
            assert response.content == "This is a test response from Claude."
            assert response.provider == AIProvider.ANTHROPIC
            assert response.model == "claude-3-haiku-20240307"
            assert response.tokens_used == 25  # input_tokens + output_tokens
            assert response.response_time is not None
            assert response.response_time > 0
            
            # Verify API call was made correctly
            mock_client.messages.create.assert_called_once()
            call_args = mock_client.messages.create.call_args[1]
            
            assert call_args['model'] == 'claude-3-haiku-20240307'
            assert call_args['temperature'] == 0.5  # From request override
            assert call_args['max_tokens'] == 100   # From request override
            assert len(call_args['messages']) == 1   # User message only
            assert call_args['messages'][0]['role'] == 'user'
            assert call_args['messages'][0]['content'] == "What is artificial intelligence?"
            assert call_args['system'] == "You are a helpful AI assistant."
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_provider_factory_pattern(self):
        """Test that Anthropic provider can be used in a factory pattern."""
        def create_provider(provider_type: AIProvider, config: AIConfig):
            """Simple factory function for creating providers."""
            if provider_type == AIProvider.ANTHROPIC:
                return AnthropicProvider(config)
            else:
                raise ValueError(f"Unsupported provider: {provider_type}")
        
        config = AIConfig(
            provider=AIProvider.ANTHROPIC,
            api_key="test-key",
            model="claude-3-haiku-20240307",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        with patch('services.anthropic_provider.Anthropic'):
            provider = create_provider(AIProvider.ANTHROPIC, config)
            
            assert isinstance(provider, AnthropicProvider)
            assert provider.config.provider == AIProvider.ANTHROPIC
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_provider_model_info_integration(self):
        """Test that model info integrates properly with the system."""
        config = AIConfig(
            provider=AIProvider.ANTHROPIC,
            api_key="test-key",
            model="claude-3-opus-20240229",
            temperature=0.8,
            max_tokens=1000,
            timeout=45,
            base_url="https://api.anthropic.com"
        )
        
        with patch('services.anthropic_provider.Anthropic'):
            provider = AnthropicProvider(config)
            model_info = provider.get_model_info()
            
            # Verify all expected fields are present
            expected_fields = [
                'provider', 'model', 'temperature', 'max_tokens', 
                'timeout', 'base_url', 'supports_system_messages',
                'supports_context', 'supports_streaming', 'model_type'
            ]
            
            for field in expected_fields:
                assert field in model_info
            
            # Verify specific values
            assert model_info['provider'] == 'anthropic'
            assert model_info['model'] == 'claude-3-opus-20240229'
            assert model_info['temperature'] == 0.8
            assert model_info['max_tokens'] == 1000
            assert model_info['timeout'] == 45
            assert model_info['base_url'] == "https://api.anthropic.com"
            assert model_info['supports_system_messages'] is True
            assert model_info['supports_context'] is True
            assert model_info['model_type'] == 'claude-3-opus'
    
    @pytest.mark.skipif(not ANTHROPIC_AVAILABLE, reason="Anthropic library not available")
    def test_provider_connection_validation_integration(self):
        """Test connection validation in integration context."""
        config = AIConfig(
            provider=AIProvider.ANTHROPIC,
            api_key="test-key",
            model="claude-3-haiku-20240307",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        # Test successful validation
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Hello"
        mock_response.stop_reason = "end_turn"
        mock_response.model = "claude-3-haiku-20240307"
        mock_response.usage = Mock()
        mock_response.usage.input_tokens = 2
        mock_response.usage.output_tokens = 3
        
        with patch('services.anthropic_provider.Anthropic') as mock_anthropic_class:
            mock_client = Mock()
            mock_anthropic_class.return_value = mock_client
            mock_client.messages.create.return_value = mock_response
            
            provider = AnthropicProvider(config)
            is_valid = provider.validate_connection()
            
            assert is_valid is True
            
            # Verify that a minimal test request was made
            mock_client.messages.create.assert_called_once()
            call_args = mock_client.messages.create.call_args[1]
            assert call_args['model'] == 'claude-3-haiku-20240307'
            assert call_args['temperature'] == 0.1  # Test uses minimal temperature
            assert call_args['max_tokens'] == 5     # Test uses minimal tokens


if __name__ == "__main__":
    pytest.main([__file__])
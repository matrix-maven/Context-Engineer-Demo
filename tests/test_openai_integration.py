"""
Integration tests for OpenAI provider with AI service infrastructure.
"""
import pytest
from unittest.mock import Mock, patch
import os

from services.openai_provider import OpenAIProvider, OPENAI_AVAILABLE
from services.ai_service import PromptRequest, ResponseStatus
from config.ai_config import AIConfig, load_ai_config
from config.settings import AIProvider


class TestOpenAIProviderIntegration:
    """Test OpenAI provider integration with the broader AI service infrastructure."""
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_provider_creation_from_config(self):
        """Test creating OpenAI provider from configuration."""
        config = AIConfig(
            provider=AIProvider.OPENAI,
            api_key="test-api-key-12345",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        with patch('services.openai_provider.OpenAI') as mock_openai:
            provider = OpenAIProvider(config)
            
            assert provider.config == config
            assert isinstance(provider, OpenAIProvider)
            mock_openai.assert_called_once()
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_provider_with_environment_config(self):
        """Test creating OpenAI provider from environment configuration."""
        # Mock environment variables
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-env-key',
            'OPENAI_MODEL': 'gpt-4',
            'AI_TEMPERATURE': '0.5',
            'AI_MAX_TOKENS': '1000'
        }):
            config = load_ai_config(AIProvider.OPENAI)
            
            assert config is not None
            assert config.provider == AIProvider.OPENAI
            assert config.get_api_key() == 'test-env-key'
            assert config.model == 'gpt-4'
            assert config.temperature == 0.5
            assert config.max_tokens == 1000
            
            with patch('services.openai_provider.OpenAI') as mock_openai:
                provider = OpenAIProvider(config)
                assert provider.config.model == 'gpt-4'
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_end_to_end_request_flow(self):
        """Test complete request flow from prompt to response."""
        config = AIConfig(
            provider=AIProvider.OPENAI,
            api_key="test-api-key",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        # Create mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "This is a test response from OpenAI."
        mock_response.choices[0].finish_reason = "stop"
        mock_response.model = "gpt-3.5-turbo"
        mock_response.usage = Mock()
        mock_response.usage.prompt_tokens = 15
        mock_response.usage.completion_tokens = 10
        mock_response.usage.total_tokens = 25
        mock_response.id = "chatcmpl-test123"
        
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response
            
            # Create provider and make request
            provider = OpenAIProvider(config)
            
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
            assert response.content == "This is a test response from OpenAI."
            assert response.provider == AIProvider.OPENAI
            assert response.model == "gpt-3.5-turbo"
            assert response.tokens_used == 25
            assert response.response_time is not None
            assert response.response_time > 0
            
            # Verify API call was made correctly
            mock_client.chat.completions.create.assert_called_once()
            call_args = mock_client.chat.completions.create.call_args[1]
            
            assert call_args['model'] == 'gpt-3.5-turbo'
            assert call_args['temperature'] == 0.5  # From request override
            assert call_args['max_tokens'] == 100   # From request override
            assert len(call_args['messages']) == 2   # System + user message
            assert call_args['messages'][0]['role'] == 'system'
            assert call_args['messages'][1]['role'] == 'user'
            assert call_args['messages'][1]['content'] == "What is artificial intelligence?"
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_provider_factory_pattern(self):
        """Test that OpenAI provider can be used in a factory pattern."""
        def create_provider(provider_type: AIProvider, config: AIConfig):
            """Simple factory function for creating providers."""
            if provider_type == AIProvider.OPENAI:
                return OpenAIProvider(config)
            else:
                raise ValueError(f"Unsupported provider: {provider_type}")
        
        config = AIConfig(
            provider=AIProvider.OPENAI,
            api_key="test-key",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        with patch('services.openai_provider.OpenAI'):
            provider = create_provider(AIProvider.OPENAI, config)
            
            assert isinstance(provider, OpenAIProvider)
            assert provider.config.provider == AIProvider.OPENAI
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_provider_model_info_integration(self):
        """Test that model info integrates properly with the system."""
        config = AIConfig(
            provider=AIProvider.OPENAI,
            api_key="test-key",
            model="gpt-4",
            temperature=0.8,
            max_tokens=1000,
            timeout=45,
            base_url="https://api.openai.com/v1"
        )
        
        with patch('services.openai_provider.OpenAI'):
            provider = OpenAIProvider(config)
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
            assert model_info['provider'] == 'openai'
            assert model_info['model'] == 'gpt-4'
            assert model_info['temperature'] == 0.8
            assert model_info['max_tokens'] == 1000
            assert model_info['timeout'] == 45
            assert model_info['base_url'] == "https://api.openai.com/v1"
            assert model_info['supports_system_messages'] is True
            assert model_info['supports_context'] is True
            assert model_info['model_type'] == 'gpt-4'
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="OpenAI library not available")
    def test_provider_connection_validation_integration(self):
        """Test connection validation in integration context."""
        config = AIConfig(
            provider=AIProvider.OPENAI,
            api_key="test-key",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            timeout=30
        )
        
        # Test successful validation
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Hello"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.model = "gpt-3.5-turbo"
        mock_response.usage = Mock()
        mock_response.usage.total_tokens = 5
        
        with patch('services.openai_provider.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response
            
            provider = OpenAIProvider(config)
            is_valid = provider.validate_connection()
            
            assert is_valid is True
            
            # Verify that a minimal test request was made
            mock_client.chat.completions.create.assert_called_once()
            call_args = mock_client.chat.completions.create.call_args[1]
            assert call_args['model'] == 'gpt-3.5-turbo'
            assert call_args['temperature'] == 0.1  # Test uses minimal temperature
            assert call_args['max_tokens'] == 5     # Test uses minimal tokens


if __name__ == "__main__":
    pytest.main([__file__])
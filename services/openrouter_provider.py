"""
OpenRouter provider implementation for AI service integration.
OpenRouter provides unified access to multiple AI models through a single API.
"""
import json
import time
from typing import Dict, Any, Optional, List
import logging

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

from .ai_service import (
    BaseAIProvider, AIResponse, PromptRequest, ResponseStatus,
    AIProviderError, AIProviderTimeoutError, AIProviderRateLimitError,
    AIProviderAuthenticationError, AIProviderInvalidRequestError
)
from config.ai_config import AIConfig
from config.settings import AIProvider


class OpenRouterProvider(BaseAIProvider):
    """
    OpenRouter provider implementation for unified AI model access.
    
    This provider handles OpenRouter API integration including authentication,
    request formatting, response parsing, and comprehensive error handling.
    OpenRouter provides access to multiple AI models through a single API.
    """
    
    def __init__(self, config: AIConfig):
        """
        Initialize OpenRouter provider with configuration.
        
        Args:
            config: AI provider configuration
            
        Raises:
            AIProviderError: If requests library is not available or config is invalid
        """
        if not REQUESTS_AVAILABLE:
            raise AIProviderError(
                "Requests library not available. Install with: pip install requests>=2.31.0",
                error_code="REQUESTS_NOT_INSTALLED",
                provider=AIProvider.OPENROUTER
            )
        
        super().__init__(config)
        
        # Set default base URL if not provided
        if not self.config.base_url:
            self.config.base_url = "https://openrouter.ai/api/v1"
        
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def _validate_config(self) -> None:
        """
        Validate OpenRouter-specific configuration.
        
        Raises:
            AIProviderError: If configuration is invalid
        """
        if self.config.provider != AIProvider.OPENROUTER:
            raise AIProviderError(
                f"Invalid provider {self.config.provider} for OpenRouterProvider",
                error_code="INVALID_PROVIDER",
                provider=self.config.provider
            )
        
        # Validate API key
        api_key = self.config.get_api_key()
        if not api_key or not api_key.strip():
            raise AIProviderError(
                "OpenRouter API key is required",
                error_code="MISSING_API_KEY",
                provider=AIProvider.OPENROUTER
            )
        
        # Validate model name
        if not self.config.model or not self.config.model.strip():
            raise AIProviderError(
                "OpenRouter model name is required",
                error_code="MISSING_MODEL",
                provider=AIProvider.OPENROUTER
            )
    
    def generate_response(self, request: PromptRequest) -> AIResponse:
        """
        Generate AI response using OpenRouter API.
        
        Args:
            request: Prompt request with context and configuration
            
        Returns:
            AIResponse: Standardized response object
            
        Raises:
            AIProviderError: If request fails
            AIProviderTimeoutError: If request times out
            AIProviderRateLimitError: If rate limit exceeded
        """
        self._log_request(request)
        
        try:
            # Prepare messages for OpenRouter (OpenAI-compatible format)
            messages = self._prepare_messages(request)
            
            # Prepare request payload
            payload = {
                'model': self.config.model,
                'messages': messages,
                'temperature': request.temperature or self.config.temperature,
                'max_tokens': request.max_tokens or self.config.max_tokens,
            }
            
            # Prepare headers
            headers = {
                'Authorization': f'Bearer {self.config.get_api_key()}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://github.com/context-engineering-demo',  # Optional: for analytics
                'X-Title': 'Context Engineering Demo'  # Optional: for analytics
            }
            
            # Make API call with timing
            response, response_time = self._measure_response_time(
                self._make_api_call, payload, headers
            )
            
            # Parse response
            ai_response = self._parse_response(response, response_time, request)
            
            self._log_response(ai_response)
            return ai_response
            
        except Exception as e:
            error_response = self._handle_error(e, request)
            self._log_response(error_response)
            return error_response
    
    def _prepare_messages(self, request: PromptRequest) -> List[Dict[str, str]]:
        """
        Prepare messages for OpenRouter API (OpenAI-compatible format).
        
        Args:
            request: Prompt request
            
        Returns:
            List of message dictionaries
        """
        messages = []
        
        # Add system message if provided
        if request.system_message:
            messages.append({
                'role': 'system',
                'content': request.system_message
            })
        
        # Add context as system message if provided and no explicit system message
        elif request.context:
            context_str = self._format_context(request.context)
            messages.append({
                'role': 'system',
                'content': f"Context information:\n{context_str}"
            })
        
        # Add user prompt
        messages.append({
            'role': 'user',
            'content': request.prompt
        })
        
        return messages
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """
        Format context dictionary into a readable string.
        
        Args:
            context: Context data
            
        Returns:
            Formatted context string
        """
        try:
            return json.dumps(context, indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            # Fallback to string representation
            return str(context)
    
    def _make_api_call(self, payload: Dict[str, Any], headers: Dict[str, str]) -> requests.Response:
        """
        Make the actual API call to OpenRouter.
        
        Args:
            payload: Request payload
            headers: Request headers
            
        Returns:
            Requests response object
            
        Raises:
            Various requests exceptions
        """
        url = f"{self.config.base_url}/chat/completions"
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.config.timeout
        )
        
        # Raise for HTTP errors
        response.raise_for_status()
        
        return response
    
    def _parse_response(self, response: requests.Response, response_time: float, 
                       request: PromptRequest) -> AIResponse:
        """
        Parse OpenRouter response into standardized format.
        
        Args:
            response: Requests response object
            response_time: Response time in seconds
            request: Original request
            
        Returns:
            Standardized AI response
        """
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            # Create a specific error for invalid JSON responses
            mapped_error = AIProviderError(
                f"Invalid JSON response from OpenRouter: {response.text}",
                error_code="INVALID_RESPONSE",
                provider=AIProvider.OPENROUTER
            )
            return self.create_error_response(mapped_error, request)
        
        # Extract content from response
        content = ""
        if 'choices' in response_data and response_data['choices']:
            choice = response_data['choices'][0]
            if 'message' in choice and 'content' in choice['message']:
                content = choice['message']['content'].strip()
        
        # Extract token usage
        tokens_used = None
        if 'usage' in response_data and response_data['usage']:
            tokens_used = response_data['usage'].get('total_tokens')
        
        # Create metadata
        metadata = {
            'model': response_data.get('model', self.config.model),
            'finish_reason': response_data['choices'][0].get('finish_reason') if response_data.get('choices') else None,
            'usage': response_data.get('usage'),
            'id': response_data.get('id'),
            'provider_used': response_data.get('provider', {}).get('name') if response_data.get('provider') else None
        }
        
        return AIResponse(
            content=content,
            provider=self.config.provider,
            model=self.config.model,
            status=ResponseStatus.SUCCESS,
            tokens_used=tokens_used,
            response_time=response_time,
            metadata=metadata
        )
    
    def _handle_error(self, error: Exception, request: Optional[PromptRequest] = None) -> AIResponse:
        """
        Handle and categorize OpenRouter API errors.
        
        Args:
            error: Exception that occurred
            request: Original request (if available)
            
        Returns:
            Standardized error response
        """
        # Handle requests exceptions
        if hasattr(error, 'response') and error.response is not None:
            status_code = error.response.status_code
            
            try:
                error_data = error.response.json()
                error_message = error_data.get('error', {}).get('message', str(error))
            except:
                error_message = str(error)
            
            # Map HTTP status codes to our custom exceptions
            if status_code == 401:
                mapped_error = AIProviderAuthenticationError(
                    f"OpenRouter authentication failed: {error_message}",
                    error_code="AUTHENTICATION_ERROR",
                    provider=AIProvider.OPENROUTER
                )
            elif status_code == 429:
                mapped_error = AIProviderRateLimitError(
                    f"OpenRouter rate limit exceeded: {error_message}",
                    error_code="RATE_LIMIT_ERROR",
                    provider=AIProvider.OPENROUTER
                )
            elif status_code == 400:
                mapped_error = AIProviderInvalidRequestError(
                    f"OpenRouter invalid request: {error_message}",
                    error_code="INVALID_REQUEST_ERROR",
                    provider=AIProvider.OPENROUTER
                )
            else:
                mapped_error = AIProviderError(
                    f"OpenRouter API error (HTTP {status_code}): {error_message}",
                    error_code="API_ERROR",
                    provider=AIProvider.OPENROUTER
                )
        
        # Handle timeout errors
        elif 'timeout' in str(error).lower() or 'timed out' in str(error).lower():
            mapped_error = AIProviderTimeoutError(
                f"OpenRouter request timed out: {str(error)}",
                error_code="TIMEOUT_ERROR",
                provider=AIProvider.OPENROUTER
            )
        
        # Generic error handling
        else:
            mapped_error = AIProviderError(
                f"OpenRouter error: {str(error)}",
                error_code="UNKNOWN_ERROR",
                provider=AIProvider.OPENROUTER
            )
        
        return self.create_error_response(mapped_error, request)
    
    def validate_connection(self) -> bool:
        """
        Validate connection to OpenRouter API.
        
        Returns:
            bool: True if connection is valid, False otherwise
        """
        try:
            # Make a minimal API call to test connection
            test_request = PromptRequest(
                prompt="Hello",
                temperature=0.1,
                max_tokens=5
            )
            
            response = self.generate_response(test_request)
            return response.success
            
        except Exception as e:
            self.logger.warning(f"OpenRouter connection validation failed: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the configured OpenRouter model.
        
        Returns:
            Dict containing model information
        """
        return {
            'provider': self.config.provider.value,
            'model': self.config.model,
            'temperature': self.config.temperature,
            'max_tokens': self.config.max_tokens,
            'timeout': self.config.timeout,
            'base_url': self.config.base_url,
            'supports_system_messages': True,
            'supports_context': True,
            'supports_streaming': False,  # Not implemented in this version
            'model_type': self._get_model_type()
        }
    
    def _get_model_type(self) -> str:
        """
        Determine the type of model being used through OpenRouter.
        
        Returns:
            Model type string
        """
        model = self.config.model.lower()
        
        # OpenRouter uses provider/model format
        if '/' in model:
            provider_part, model_part = model.split('/', 1)
            
            if 'openai' in provider_part:
                if 'gpt-4' in model_part:
                    return 'openai-gpt-4'
                elif 'gpt-3.5' in model_part:
                    return 'openai-gpt-3.5'
                else:
                    return 'openai'
            elif 'anthropic' in provider_part:
                return 'anthropic-claude'
            elif 'google' in provider_part:
                return 'google-gemini'
            elif 'meta' in provider_part:
                return 'meta-llama'
            else:
                return provider_part
        else:
            return 'openrouter'
    
    def __str__(self) -> str:
        """String representation of OpenRouter provider."""
        return f"OpenRouterProvider(model={self.config.model})"
    
    def __repr__(self) -> str:
        """Detailed string representation of OpenRouter provider."""
        return (
            f"OpenRouterProvider("
            f"model={self.config.model}, "
            f"temperature={self.config.temperature}, "
            f"max_tokens={self.config.max_tokens}, "
            f"timeout={self.config.timeout})"
        )
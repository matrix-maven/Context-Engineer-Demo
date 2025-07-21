"""
OpenAI provider implementation for AI service integration.
"""
import json
import time
from typing import Dict, Any, Optional, List
import logging

try:
    import openai
    from openai import OpenAI
    from openai.types.chat import ChatCompletion
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None
    ChatCompletion = None

from .ai_service import (
    BaseAIProvider, AIResponse, PromptRequest, ResponseStatus,
    AIProviderError, AIProviderTimeoutError, AIProviderRateLimitError,
    AIProviderAuthenticationError, AIProviderInvalidRequestError
)
from config.ai_config import AIConfig
from config.settings import AIProvider


class OpenAIProvider(BaseAIProvider):
    """
    OpenAI provider implementation with GPT model support.
    
    This provider handles OpenAI API integration including authentication,
    request formatting, response parsing, and comprehensive error handling.
    """
    
    def __init__(self, config: AIConfig):
        """
        Initialize OpenAI provider with configuration.
        
        Args:
            config: AI provider configuration
            
        Raises:
            AIProviderError: If OpenAI library is not available or config is invalid
        """
        if not OPENAI_AVAILABLE:
            raise AIProviderError(
                "OpenAI library not available. Install with: pip install openai>=1.0.0",
                error_code="OPENAI_NOT_INSTALLED",
                provider=AIProvider.OPENAI
            )
        
        super().__init__(config)
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=self.config.get_api_key(),
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )
        
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def _validate_config(self) -> None:
        """
        Validate OpenAI-specific configuration.
        
        Raises:
            AIProviderError: If configuration is invalid
        """
        if self.config.provider != AIProvider.OPENAI:
            raise AIProviderError(
                f"Invalid provider {self.config.provider} for OpenAIProvider",
                error_code="INVALID_PROVIDER",
                provider=self.config.provider
            )
        
        # Validate API key
        api_key = self.config.get_api_key()
        if not api_key or not api_key.strip():
            raise AIProviderError(
                "OpenAI API key is required",
                error_code="MISSING_API_KEY",
                provider=AIProvider.OPENAI
            )
        
        # Validate model name
        if not self.config.model or not self.config.model.strip():
            raise AIProviderError(
                "OpenAI model name is required",
                error_code="MISSING_MODEL",
                provider=AIProvider.OPENAI
            )
        
        # Validate model format (basic check)
        valid_prefixes = ['gpt-', 'text-', 'davinci', 'curie', 'babbage', 'ada']
        if not any(self.config.model.startswith(prefix) for prefix in valid_prefixes):
            self.logger.warning(f"Unusual OpenAI model name: {self.config.model}")
    
    def generate_response(self, request: PromptRequest) -> AIResponse:
        """
        Generate AI response using OpenAI API.
        
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
            # Prepare messages for chat completion
            messages = self._prepare_messages(request)
            
            # Prepare request parameters
            request_params = {
                'model': self.config.model,
                'messages': messages,
                'temperature': request.temperature or self.config.temperature,
                'max_tokens': request.max_tokens or self.config.max_tokens,
            }
            
            # Make API call with timing
            response, response_time = self._measure_response_time(
                self._make_api_call, request_params
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
        Prepare messages for OpenAI chat completion API.
        
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
    
    def _make_api_call(self, request_params: Dict[str, Any]) -> ChatCompletion:
        """
        Make the actual API call to OpenAI.
        
        Args:
            request_params: Request parameters
            
        Returns:
            OpenAI chat completion response
            
        Raises:
            Various OpenAI exceptions
        """
        return self.client.chat.completions.create(**request_params)
    
    def _parse_response(self, response: ChatCompletion, response_time: float, 
                       request: PromptRequest) -> AIResponse:
        """
        Parse OpenAI response into standardized format.
        
        Args:
            response: OpenAI chat completion response
            response_time: Response time in seconds
            request: Original request
            
        Returns:
            Standardized AI response
        """
        # Extract content from response
        content = ""
        if response.choices and len(response.choices) > 0:
            choice = response.choices[0]
            if choice.message and choice.message.content:
                content = choice.message.content.strip()
        
        # Extract token usage
        tokens_used = None
        if response.usage:
            tokens_used = response.usage.total_tokens
        
        # Create metadata
        metadata = {
            'model': response.model,
            'finish_reason': response.choices[0].finish_reason if response.choices else None,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens if response.usage else None,
                'completion_tokens': response.usage.completion_tokens if response.usage else None,
                'total_tokens': response.usage.total_tokens if response.usage else None
            } if response.usage else None,
            'request_id': getattr(response, 'id', None)
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
        Handle and categorize OpenAI API errors.
        
        Args:
            error: Exception that occurred
            request: Original request (if available)
            
        Returns:
            Standardized error response
        """
        # Map OpenAI exceptions to our custom exceptions
        if hasattr(error, '__class__'):
            error_name = error.__class__.__name__
            
            # Authentication errors
            if 'AuthenticationError' in error_name or 'PermissionDeniedError' in error_name:
                mapped_error = AIProviderAuthenticationError(
                    f"OpenAI authentication failed: {str(error)}",
                    error_code="AUTHENTICATION_ERROR",
                    provider=AIProvider.OPENAI
                )
            
            # Rate limit errors
            elif 'RateLimitError' in error_name:
                mapped_error = AIProviderRateLimitError(
                    f"OpenAI rate limit exceeded: {str(error)}",
                    error_code="RATE_LIMIT_ERROR",
                    provider=AIProvider.OPENAI
                )
            
            # Timeout errors
            elif 'TimeoutError' in error_name or 'timeout' in str(error).lower():
                mapped_error = AIProviderTimeoutError(
                    f"OpenAI request timed out: {str(error)}",
                    error_code="TIMEOUT_ERROR",
                    provider=AIProvider.OPENAI
                )
            
            # Invalid request errors
            elif 'BadRequestError' in error_name or 'InvalidRequestError' in error_name:
                mapped_error = AIProviderInvalidRequestError(
                    f"OpenAI invalid request: {str(error)}",
                    error_code="INVALID_REQUEST_ERROR",
                    provider=AIProvider.OPENAI
                )
            
            # Generic API errors
            else:
                mapped_error = AIProviderError(
                    f"OpenAI API error: {str(error)}",
                    error_code="API_ERROR",
                    provider=AIProvider.OPENAI
                )
        else:
            # Unknown error type
            mapped_error = AIProviderError(
                f"Unknown OpenAI error: {str(error)}",
                error_code="UNKNOWN_ERROR",
                provider=AIProvider.OPENAI
            )
        
        return self.create_error_response(mapped_error, request)
    
    def validate_connection(self) -> bool:
        """
        Validate connection to OpenAI API.
        
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
            self.logger.warning(f"OpenAI connection validation failed: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the configured OpenAI model.
        
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
        Determine the type of OpenAI model being used.
        
        Returns:
            Model type string
        """
        model = self.config.model.lower()
        
        if model.startswith('gpt-4'):
            return 'gpt-4'
        elif model.startswith('gpt-3.5'):
            return 'gpt-3.5'
        elif model.startswith('text-'):
            return 'completion'
        elif model in ['davinci', 'curie', 'babbage', 'ada']:
            return 'legacy'
        else:
            return 'unknown'
    
    def __str__(self) -> str:
        """String representation of OpenAI provider."""
        return f"OpenAIProvider(model={self.config.model})"
    
    def __repr__(self) -> str:
        """Detailed string representation of OpenAI provider."""
        return (
            f"OpenAIProvider("
            f"model={self.config.model}, "
            f"temperature={self.config.temperature}, "
            f"max_tokens={self.config.max_tokens}, "
            f"timeout={self.config.timeout})"
        )
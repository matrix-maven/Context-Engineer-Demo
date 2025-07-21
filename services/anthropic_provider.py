"""
Anthropic provider implementation for AI service integration.
"""
import json
import time
from typing import Dict, Any, Optional, List
import logging

try:
    import anthropic
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None

from .ai_service import (
    BaseAIProvider, AIResponse, PromptRequest, ResponseStatus,
    AIProviderError, AIProviderTimeoutError, AIProviderRateLimitError,
    AIProviderAuthenticationError, AIProviderInvalidRequestError
)
from config.ai_config import AIConfig
from config.settings import AIProvider


class AnthropicProvider(BaseAIProvider):
    """
    Anthropic provider implementation with Claude model support.
    
    This provider handles Anthropic API integration including authentication,
    request formatting, response parsing, and comprehensive error handling.
    """
    
    def __init__(self, config: AIConfig):
        """
        Initialize Anthropic provider with configuration.
        
        Args:
            config: AI provider configuration
            
        Raises:
            AIProviderError: If Anthropic library is not available or config is invalid
        """
        if not ANTHROPIC_AVAILABLE:
            raise AIProviderError(
                "Anthropic library not available. Install with: pip install anthropic>=0.7.0",
                error_code="ANTHROPIC_NOT_INSTALLED",
                provider=AIProvider.ANTHROPIC
            )
        
        super().__init__(config)
        
        # Initialize Anthropic client
        self.client = Anthropic(
            api_key=self.config.get_api_key(),
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )
        
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def _validate_config(self) -> None:
        """
        Validate Anthropic-specific configuration.
        
        Raises:
            AIProviderError: If configuration is invalid
        """
        if self.config.provider != AIProvider.ANTHROPIC:
            raise AIProviderError(
                f"Invalid provider {self.config.provider} for AnthropicProvider",
                error_code="INVALID_PROVIDER",
                provider=self.config.provider
            )
        
        # Validate API key
        api_key = self.config.get_api_key()
        if not api_key or not api_key.strip():
            raise AIProviderError(
                "Anthropic API key is required",
                error_code="MISSING_API_KEY",
                provider=AIProvider.ANTHROPIC
            )
        
        # Validate model name
        if not self.config.model or not self.config.model.strip():
            raise AIProviderError(
                "Anthropic model name is required",
                error_code="MISSING_MODEL",
                provider=AIProvider.ANTHROPIC
            )
        
        # Validate model format (basic check)
        if not self.config.model.startswith('claude'):
            self.logger.warning(f"Unusual Anthropic model name: {self.config.model}")
    
    def generate_response(self, request: PromptRequest) -> AIResponse:
        """
        Generate AI response using Anthropic API.
        
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
            # Prepare messages for Claude
            messages = self._prepare_messages(request)
            system_message = self._prepare_system_message(request)
            
            # Prepare request parameters
            request_params = {
                'model': self.config.model,
                'messages': messages,
                'max_tokens': request.max_tokens or self.config.max_tokens,
                'temperature': request.temperature or self.config.temperature,
            }
            
            # Add system message if present
            if system_message:
                request_params['system'] = system_message
            
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
        Prepare messages for Anthropic API.
        
        Args:
            request: Prompt request
            
        Returns:
            List of message dictionaries
        """
        messages = []
        
        # Add user prompt (context will be handled in system message)
        messages.append({
            'role': 'user',
            'content': request.prompt
        })
        
        return messages
    
    def _prepare_system_message(self, request: PromptRequest) -> Optional[str]:
        """
        Prepare system message for Anthropic API.
        
        Args:
            request: Prompt request
            
        Returns:
            System message string or None
        """
        system_parts = []
        
        # Add explicit system message if provided
        if request.system_message:
            system_parts.append(request.system_message)
        
        # Add context as system message if provided
        if request.context:
            context_str = self._format_context(request.context)
            system_parts.append(f"Context information:\n{context_str}")
        
        return "\n\n".join(system_parts) if system_parts else None
    
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
    
    def _make_api_call(self, request_params: Dict[str, Any]):
        """
        Make the actual API call to Anthropic.
        
        Args:
            request_params: Request parameters
            
        Returns:
            Anthropic message response
            
        Raises:
            Various Anthropic exceptions
        """
        return self.client.messages.create(**request_params)
    
    def _parse_response(self, response, response_time: float, 
                       request: PromptRequest) -> AIResponse:
        """
        Parse Anthropic response into standardized format.
        
        Args:
            response: Anthropic message response
            response_time: Response time in seconds
            request: Original request
            
        Returns:
            Standardized AI response
        """
        # Extract content from response
        content = ""
        if hasattr(response, 'content') and response.content:
            # Anthropic returns content as a list of content blocks
            content_blocks = []
            for block in response.content:
                if hasattr(block, 'text'):
                    content_blocks.append(block.text)
            content = "".join(content_blocks).strip()
        
        # Extract token usage
        tokens_used = None
        if hasattr(response, 'usage') and response.usage:
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
        
        # Create metadata
        metadata = {
            'model': response.model if hasattr(response, 'model') else self.config.model,
            'stop_reason': response.stop_reason if hasattr(response, 'stop_reason') else None,
            'usage': {
                'input_tokens': response.usage.input_tokens if hasattr(response, 'usage') and response.usage else None,
                'output_tokens': response.usage.output_tokens if hasattr(response, 'usage') and response.usage else None,
                'total_tokens': tokens_used
            } if hasattr(response, 'usage') and response.usage else None,
            'message_id': response.id if hasattr(response, 'id') else None
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
        Handle and categorize Anthropic API errors.
        
        Args:
            error: Exception that occurred
            request: Original request (if available)
            
        Returns:
            Standardized error response
        """
        # Map Anthropic exceptions to our custom exceptions
        if hasattr(error, '__class__'):
            error_name = error.__class__.__name__
            error_str = str(error).lower()
            
            # Authentication errors
            if 'authentication' in error_str or 'unauthorized' in error_str or 'permission' in error_str:
                mapped_error = AIProviderAuthenticationError(
                    f"Anthropic authentication failed: {str(error)}",
                    error_code="AUTHENTICATION_ERROR",
                    provider=AIProvider.ANTHROPIC
                )
            
            # Rate limit errors
            elif 'rate limit' in error_str or 'too many requests' in error_str:
                mapped_error = AIProviderRateLimitError(
                    f"Anthropic rate limit exceeded: {str(error)}",
                    error_code="RATE_LIMIT_ERROR",
                    provider=AIProvider.ANTHROPIC
                )
            
            # Timeout errors
            elif 'timeout' in error_str or 'timed out' in error_str:
                mapped_error = AIProviderTimeoutError(
                    f"Anthropic request timed out: {str(error)}",
                    error_code="TIMEOUT_ERROR",
                    provider=AIProvider.ANTHROPIC
                )
            
            # Invalid request errors
            elif 'bad request' in error_str or 'invalid' in error_str:
                mapped_error = AIProviderInvalidRequestError(
                    f"Anthropic invalid request: {str(error)}",
                    error_code="INVALID_REQUEST_ERROR",
                    provider=AIProvider.ANTHROPIC
                )
            
            # Generic API errors
            else:
                mapped_error = AIProviderError(
                    f"Anthropic API error: {str(error)}",
                    error_code="API_ERROR",
                    provider=AIProvider.ANTHROPIC
                )
        else:
            # Unknown error type
            mapped_error = AIProviderError(
                f"Unknown Anthropic error: {str(error)}",
                error_code="UNKNOWN_ERROR",
                provider=AIProvider.ANTHROPIC
            )
        
        return self.create_error_response(mapped_error, request)
    
    def validate_connection(self) -> bool:
        """
        Validate connection to Anthropic API.
        
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
            self.logger.warning(f"Anthropic connection validation failed: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the configured Anthropic model.
        
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
        Determine the type of Anthropic model being used.
        
        Returns:
            Model type string
        """
        model = self.config.model.lower()
        
        if 'claude-3' in model:
            if 'opus' in model:
                return 'claude-3-opus'
            elif 'sonnet' in model:
                return 'claude-3-sonnet'
            elif 'haiku' in model:
                return 'claude-3-haiku'
            else:
                return 'claude-3'
        elif 'claude-2' in model:
            return 'claude-2'
        elif 'claude-instant' in model:
            return 'claude-instant'
        else:
            return 'claude'
    
    def __str__(self) -> str:
        """String representation of Anthropic provider."""
        return f"AnthropicProvider(model={self.config.model})"
    
    def __repr__(self) -> str:
        """Detailed string representation of Anthropic provider."""
        return (
            f"AnthropicProvider("
            f"model={self.config.model}, "
            f"temperature={self.config.temperature}, "
            f"max_tokens={self.config.max_tokens}, "
            f"timeout={self.config.timeout})"
        )
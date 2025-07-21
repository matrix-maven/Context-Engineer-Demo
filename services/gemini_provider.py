"""
Google Gemini provider implementation for AI service integration.
"""
import json
import time
from typing import Dict, Any, Optional, List
import logging

try:
    import google.generativeai as genai
    from google.generativeai.types import GenerateContentResponse
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    GenerateContentResponse = None

from .ai_service import (
    BaseAIProvider, AIResponse, PromptRequest, ResponseStatus,
    AIProviderError, AIProviderTimeoutError, AIProviderRateLimitError,
    AIProviderAuthenticationError, AIProviderInvalidRequestError
)
from config.ai_config import AIConfig
from config.settings import AIProvider


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini provider implementation.
    
    This provider handles Google Gemini API integration including authentication,
    request formatting, response parsing, and comprehensive error handling.
    """
    
    def __init__(self, config: AIConfig):
        """
        Initialize Gemini provider with configuration.
        
        Args:
            config: AI provider configuration
            
        Raises:
            AIProviderError: If Gemini library is not available or config is invalid
        """
        if not GEMINI_AVAILABLE:
            raise AIProviderError(
                "Google Gemini library not available. Install with: pip install google-generativeai>=0.3.0",
                error_code="GEMINI_NOT_INSTALLED",
                provider=AIProvider.GEMINI
            )
        
        super().__init__(config)
        
        # Configure Gemini API
        genai.configure(api_key=self.config.get_api_key())
        
        # Initialize model
        self.model = genai.GenerativeModel(self.config.model)
        
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def _validate_config(self) -> None:
        """
        Validate Gemini-specific configuration.
        
        Raises:
            AIProviderError: If configuration is invalid
        """
        if self.config.provider != AIProvider.GEMINI:
            raise AIProviderError(
                f"Invalid provider {self.config.provider} for GeminiProvider",
                error_code="INVALID_PROVIDER",
                provider=self.config.provider
            )
        
        # Validate API key
        api_key = self.config.get_api_key()
        if not api_key or not api_key.strip():
            raise AIProviderError(
                "Gemini API key is required",
                error_code="MISSING_API_KEY",
                provider=AIProvider.GEMINI
            )
        
        # Validate model name
        if not self.config.model or not self.config.model.strip():
            raise AIProviderError(
                "Gemini model name is required",
                error_code="MISSING_MODEL",
                provider=AIProvider.GEMINI
            )
        
        # Validate model format (basic check)
        if not self.config.model.startswith('gemini'):
            self.logger.warning(f"Unusual Gemini model name: {self.config.model}")
    
    def generate_response(self, request: PromptRequest) -> AIResponse:
        """
        Generate AI response using Gemini API.
        
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
            # Prepare prompt for Gemini
            prompt = self._prepare_prompt(request)
            
            # Prepare generation config
            generation_config = {
                'temperature': request.temperature or self.config.temperature,
                'max_output_tokens': request.max_tokens or self.config.max_tokens,
            }
            
            # Make API call with timing
            response, response_time = self._measure_response_time(
                self._make_api_call, prompt, generation_config
            )
            
            # Parse response
            ai_response = self._parse_response(response, response_time, request)
            
            self._log_response(ai_response)
            return ai_response
            
        except Exception as e:
            error_response = self._handle_error(e, request)
            self._log_response(error_response)
            return error_response
    
    def _prepare_prompt(self, request: PromptRequest) -> str:
        """
        Prepare prompt for Gemini API.
        
        Args:
            request: Prompt request
            
        Returns:
            Combined prompt string
        """
        prompt_parts = []
        
        # Add system message if provided
        if request.system_message:
            prompt_parts.append(f"System: {request.system_message}")
        
        # Add context if provided
        if request.context:
            context_str = self._format_context(request.context)
            prompt_parts.append(f"Context: {context_str}")
        
        # Add user prompt
        prompt_parts.append(f"User: {request.prompt}")
        
        return "\n\n".join(prompt_parts)
    
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
    
    def _make_api_call(self, prompt: str, generation_config: Dict[str, Any]) -> GenerateContentResponse:
        """
        Make the actual API call to Gemini.
        
        Args:
            prompt: Prepared prompt string
            generation_config: Generation configuration
            
        Returns:
            Gemini generate content response
            
        Raises:
            Various Gemini exceptions
        """
        return self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
    
    def _parse_response(self, response: GenerateContentResponse, response_time: float, 
                       request: PromptRequest) -> AIResponse:
        """
        Parse Gemini response into standardized format.
        
        Args:
            response: Gemini generate content response
            response_time: Response time in seconds
            request: Original request
            
        Returns:
            Standardized AI response
        """
        # Extract content from response
        content = ""
        if hasattr(response, 'text') and response.text:
            content = response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            # Extract from candidates if text is not directly available
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content:
                if hasattr(candidate.content, 'parts') and candidate.content.parts:
                    content = candidate.content.parts[0].text.strip()
        
        # Extract token usage (if available)
        tokens_used = None
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            tokens_used = (
                response.usage_metadata.prompt_token_count + 
                response.usage_metadata.candidates_token_count
            )
        
        # Create metadata
        metadata = {
            'model': self.config.model,
            'finish_reason': None,
            'usage': {
                'prompt_tokens': response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') and response.usage_metadata else None,
                'completion_tokens': response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') and response.usage_metadata else None,
                'total_tokens': tokens_used
            } if hasattr(response, 'usage_metadata') and response.usage_metadata else None,
        }
        
        # Add finish reason if available
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'finish_reason'):
                metadata['finish_reason'] = str(candidate.finish_reason)
        
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
        Handle and categorize Gemini API errors.
        
        Args:
            error: Exception that occurred
            request: Original request (if available)
            
        Returns:
            Standardized error response
        """
        # Map Gemini exceptions to our custom exceptions
        error_str = str(error).lower()
        
        # Authentication errors
        if 'api key' in error_str or 'authentication' in error_str or 'unauthorized' in error_str:
            mapped_error = AIProviderAuthenticationError(
                f"Gemini authentication failed: {str(error)}",
                error_code="AUTHENTICATION_ERROR",
                provider=AIProvider.GEMINI
            )
        
        # Rate limit errors
        elif 'quota' in error_str or 'rate limit' in error_str or 'too many requests' in error_str:
            mapped_error = AIProviderRateLimitError(
                f"Gemini rate limit exceeded: {str(error)}",
                error_code="RATE_LIMIT_ERROR",
                provider=AIProvider.GEMINI
            )
        
        # Timeout errors
        elif 'timeout' in error_str or 'timed out' in error_str:
            mapped_error = AIProviderTimeoutError(
                f"Gemini request timed out: {str(error)}",
                error_code="TIMEOUT_ERROR",
                provider=AIProvider.GEMINI
            )
        
        # Invalid request errors
        elif 'invalid' in error_str or 'bad request' in error_str:
            mapped_error = AIProviderInvalidRequestError(
                f"Gemini invalid request: {str(error)}",
                error_code="INVALID_REQUEST_ERROR",
                provider=AIProvider.GEMINI
            )
        
        # Generic API errors
        else:
            mapped_error = AIProviderError(
                f"Gemini API error: {str(error)}",
                error_code="API_ERROR",
                provider=AIProvider.GEMINI
            )
        
        return self.create_error_response(mapped_error, request)
    
    def validate_connection(self) -> bool:
        """
        Validate connection to Gemini API.
        
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
            self.logger.warning(f"Gemini connection validation failed: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the configured Gemini model.
        
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
        Determine the type of Gemini model being used.
        
        Returns:
            Model type string
        """
        model = self.config.model.lower()
        
        if 'gemini-1.5-pro' in model:
            return 'gemini-1.5-pro'
        elif 'gemini-1.5-flash' in model:
            return 'gemini-1.5-flash'
        elif 'gemini-pro' in model:
            return 'gemini-pro'
        elif 'gemini-ultra' in model:
            return 'gemini-ultra'
        elif 'gemini' in model:
            return 'gemini'
        else:
            return 'unknown'
    
    def __str__(self) -> str:
        """String representation of Gemini provider."""
        return f"GeminiProvider(model={self.config.model})"
    
    def __repr__(self) -> str:
        """Detailed string representation of Gemini provider."""
        return (
            f"GeminiProvider("
            f"model={self.config.model}, "
            f"temperature={self.config.temperature}, "
            f"max_tokens={self.config.max_tokens}, "
            f"timeout={self.config.timeout})"
        )
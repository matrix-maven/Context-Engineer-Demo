"""
AI service infrastructure with abstract provider interface and response models.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime, timezone
from enum import Enum
import time
import logging

from config.ai_config import AIConfig
from config.settings import AIProvider


class ResponseStatus(str, Enum):
    """AI response status enumeration."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    INVALID_REQUEST = "invalid_request"


@dataclass
class AIResponse:
    """
    Standardized AI response data model.
    
    This class represents the response from any AI provider with consistent
    structure for error handling and metrics tracking.
    """
    content: str
    provider: AIProvider
    model: str
    status: ResponseStatus
    tokens_used: Optional[int] = None
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
    
    @property
    def success(self) -> bool:
        """Check if response was successful."""
        return self.status == ResponseStatus.SUCCESS
    
    @property
    def has_error(self) -> bool:
        """Check if response has an error."""
        return self.status != ResponseStatus.SUCCESS
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary for serialization."""
        return {
            'content': self.content,
            'provider': self.provider.value,
            'model': self.model,
            'status': self.status.value,
            'tokens_used': self.tokens_used,
            'response_time': self.response_time,
            'error_message': self.error_message,
            'error_code': self.error_code,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'metadata': self.metadata or {}
        }


@dataclass
class PromptRequest:
    """
    Standardized prompt request data model.
    
    This class represents a request to an AI provider with all necessary
    context and configuration.
    """
    prompt: str
    context: Optional[Dict[str, Any]] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    system_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        return {
            'prompt': self.prompt,
            'context': self.context or {},
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'system_message': self.system_message,
            'metadata': self.metadata or {}
        }


class AIProviderError(Exception):
    """Base exception for AI provider errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 provider: Optional[AIProvider] = None):
        super().__init__(message)
        self.error_code = error_code
        self.provider = provider
        self.timestamp = datetime.now(timezone.utc)


class AIProviderTimeoutError(AIProviderError):
    """Exception raised when AI provider request times out."""
    pass


class AIProviderRateLimitError(AIProviderError):
    """Exception raised when AI provider rate limit is exceeded."""
    pass


class AIProviderAuthenticationError(AIProviderError):
    """Exception raised when AI provider authentication fails."""
    pass


class AIProviderInvalidRequestError(AIProviderError):
    """Exception raised when AI provider request is invalid."""
    pass


class BaseAIProvider(ABC):
    """
    Abstract base class for AI providers.
    
    This class defines the standard interface that all AI providers must implement
    to ensure consistent behavior across different AI services.
    """
    
    def __init__(self, config: AIConfig):
        """
        Initialize AI provider with configuration.
        
        Args:
            config: AI provider configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._validate_config()
    
    @abstractmethod
    def _validate_config(self) -> None:
        """
        Validate provider-specific configuration.
        
        Raises:
            AIProviderError: If configuration is invalid
        """
        pass
    
    @abstractmethod
    def generate_response(self, request: PromptRequest) -> AIResponse:
        """
        Generate AI response for the given prompt request.
        
        Args:
            request: Prompt request with context and configuration
            
        Returns:
            AIResponse: Standardized response object
            
        Raises:
            AIProviderError: If request fails
            AIProviderTimeoutError: If request times out
            AIProviderRateLimitError: If rate limit exceeded
        """
        pass
    
    @abstractmethod
    def validate_connection(self) -> bool:
        """
        Validate connection to AI provider.
        
        Returns:
            bool: True if connection is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the configured model.
        
        Returns:
            Dict containing model information
        """
        pass
    
    def create_error_response(self, error: Exception, 
                            request: Optional[PromptRequest] = None) -> AIResponse:
        """
        Create standardized error response.
        
        Args:
            error: Exception that occurred
            request: Original request (if available)
            
        Returns:
            AIResponse: Error response object
        """
        # Determine status based on error type
        if isinstance(error, AIProviderTimeoutError):
            status = ResponseStatus.TIMEOUT
        elif isinstance(error, AIProviderRateLimitError):
            status = ResponseStatus.RATE_LIMITED
        elif isinstance(error, AIProviderInvalidRequestError):
            status = ResponseStatus.INVALID_REQUEST
        else:
            status = ResponseStatus.ERROR
        
        # Extract error details
        error_message = str(error)
        error_code = getattr(error, 'error_code', None)
        
        return AIResponse(
            content="",
            provider=self.config.provider,
            model=self.config.model,
            status=status,
            error_message=error_message,
            error_code=error_code,
            metadata={'request': request.to_dict() if request else None}
        )
    
    def _measure_response_time(self, func, *args, **kwargs):
        """
        Measure response time for a function call.
        
        Args:
            func: Function to measure
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Tuple of (result, response_time)
        """
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            response_time = time.time() - start_time
            return result, response_time
        except Exception as e:
            response_time = time.time() - start_time
            # Add response time to error metadata if it's an AIProviderError
            if isinstance(e, AIProviderError):
                if not hasattr(e, 'metadata'):
                    e.metadata = {}
                e.metadata['response_time'] = response_time
            raise
    
    def _log_request(self, request: PromptRequest) -> None:
        """Log request details (without sensitive information)."""
        self.logger.debug(
            f"AI request to {self.config.provider.value}: "
            f"model={self.config.model}, "
            f"prompt_length={len(request.prompt)}, "
            f"has_context={bool(request.context)}"
        )
    
    def _log_response(self, response: AIResponse) -> None:
        """Log response details."""
        if response.success:
            self.logger.debug(
                f"AI response from {response.provider.value}: "
                f"status={response.status.value}, "
                f"tokens={response.tokens_used}, "
                f"time={response.response_time:.2f}s"
            )
        else:
            self.logger.warning(
                f"AI error from {response.provider.value}: "
                f"status={response.status.value}, "
                f"error={response.error_message}"
            )
    
    def __str__(self) -> str:
        """String representation of provider."""
        return f"{self.__class__.__name__}(provider={self.config.provider.value}, model={self.config.model})"
    
    def __repr__(self) -> str:
        """Detailed string representation of provider."""
        return (
            f"{self.__class__.__name__}("
            f"provider={self.config.provider.value}, "
            f"model={self.config.model}, "
            f"temperature={self.config.temperature}, "
            f"max_tokens={self.config.max_tokens})"
        )


# Type alias for provider factory functions
ProviderFactory = Callable[[AIConfig], BaseAIProvider]
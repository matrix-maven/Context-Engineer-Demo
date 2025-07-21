"""
AI Service Orchestrator for managing multiple AI providers.

This module provides a unified interface for working with multiple AI providers,
including provider switching, fallback logic, response caching, and comprehensive
error handling and logging.
"""
import logging
import time
from typing import Dict, List, Optional, Any, Type, Union
from datetime import datetime, timedelta
from functools import lru_cache
import hashlib
import json

from .ai_service import (
    BaseAIProvider, AIResponse, PromptRequest, ResponseStatus,
    AIProviderError, AIProviderTimeoutError, AIProviderRateLimitError,
    AIProviderAuthenticationError, AIProviderInvalidRequestError
)
from .openai_provider import OpenAIProvider, OPENAI_AVAILABLE
from .anthropic_provider import AnthropicProvider, ANTHROPIC_AVAILABLE
from .gemini_provider import GeminiProvider, GEMINI_AVAILABLE
from .openrouter_provider import OpenRouterProvider, REQUESTS_AVAILABLE
from config.ai_config import AIConfig, load_ai_config, get_available_providers, get_default_provider
from config.settings import AIProvider
from utils.error_recovery import ErrorRecoveryManager, RecoveryConfig
from utils.error_handler import ErrorHandler


class AIServiceOrchestrator:
    """
    AI Service Orchestrator for managing multiple AI providers.
    
    This class provides a unified interface for working with multiple AI providers,
    including automatic provider switching, fallback logic, response caching,
    and comprehensive error handling.
    """
    
    def __init__(self, 
                 default_provider: Optional[AIProvider] = None,
                 enable_caching: bool = True,
                 cache_ttl_seconds: int = 300,
                 max_retries: int = 2,
                 fallback_enabled: bool = True):
        """
        Initialize the AI Service Orchestrator.
        
        Args:
            default_provider: Default AI provider to use
            enable_caching: Whether to enable response caching
            cache_ttl_seconds: Cache time-to-live in seconds
            max_retries: Maximum number of retries for failed requests
            fallback_enabled: Whether to enable automatic fallback to other providers
        """
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        
        # Configuration
        self.enable_caching = enable_caching
        self.cache_ttl_seconds = cache_ttl_seconds
        self.max_retries = max_retries
        self.fallback_enabled = fallback_enabled
        
        # Provider management
        self.providers: Dict[AIProvider, BaseAIProvider] = {}
        self.provider_configs: Dict[AIProvider, AIConfig] = {}
        self.current_provider: Optional[AIProvider] = None
        
        # Response cache
        self.response_cache: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.provider_stats: Dict[AIProvider, Dict[str, Any]] = {}
        
        # Error recovery manager
        recovery_config = RecoveryConfig(
            max_retries=max_retries,
            enable_fallback=fallback_enabled,
            enable_caching=enable_caching,
            cache_ttl=cache_ttl_seconds
        )
        self.recovery_manager = ErrorRecoveryManager(recovery_config)
        
        # Initialize providers
        self._initialize_providers()
        
        # Set default provider
        if default_provider:
            self.set_provider(default_provider)
        else:
            # Use system default or first available
            default = get_default_provider()
            if default:
                self.set_provider(default)
            elif self.providers:
                self.set_provider(list(self.providers.keys())[0])
    
    def _initialize_providers(self) -> None:
        """Initialize all available AI providers."""
        self.logger.info("Initializing AI providers...")
        
        # Load all available configurations
        available_providers = get_available_providers()
        
        for provider in available_providers:
            try:
                config = load_ai_config(provider)
                if config:
                    provider_instance = self._create_provider_instance(provider, config)
                    if provider_instance:
                        self.providers[provider] = provider_instance
                        self.provider_configs[provider] = config
                        self.provider_stats[provider] = {
                            'requests': 0,
                            'successes': 0,
                            'failures': 0,
                            'total_response_time': 0.0,
                            'average_response_time': 0.0,
                            'last_used': None,
                            'consecutive_failures': 0
                        }
                        # Register provider with error recovery manager
                        self.recovery_manager.register_provider(provider.value)
                        self.logger.info(f"✅ Initialized {provider.value} provider")
                    else:
                        self.logger.warning(f"⚠️  Failed to create {provider.value} provider instance")
                else:
                    self.logger.warning(f"⚠️  No configuration found for {provider.value}")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize {provider.value} provider: {e}")
        
        self.logger.info(f"Initialized {len(self.providers)} AI providers: {list(self.providers.keys())}")
    
    def _create_provider_instance(self, provider: AIProvider, config: AIConfig) -> Optional[BaseAIProvider]:
        """
        Create a provider instance based on the provider type.
        
        Args:
            provider: AI provider type
            config: Provider configuration
            
        Returns:
            Provider instance or None if creation fails
        """
        try:
            if provider == AIProvider.OPENAI and OPENAI_AVAILABLE:
                return OpenAIProvider(config)
            elif provider == AIProvider.ANTHROPIC and ANTHROPIC_AVAILABLE:
                return AnthropicProvider(config)
            elif provider == AIProvider.GEMINI and GEMINI_AVAILABLE:
                return GeminiProvider(config)
            elif provider == AIProvider.OPENROUTER and REQUESTS_AVAILABLE:
                return OpenRouterProvider(config)
            else:
                self.logger.warning(f"Provider {provider.value} not available or library not installed")
                return None
        except Exception as e:
            self.logger.error(f"Failed to create {provider.value} provider: {e}")
            return None
    
    def set_provider(self, provider: AIProvider) -> bool:
        """
        Set the current AI provider.
        
        Args:
            provider: AI provider to use
            
        Returns:
            bool: True if provider was set successfully, False otherwise
        """
        if provider not in self.providers:
            self.logger.error(f"Provider {provider.value} not available")
            return False
        
        self.current_provider = provider
        self.logger.info(f"Set current provider to {provider.value}")
        return True
    
    def get_current_provider(self) -> Optional[AIProvider]:
        """
        Get the current AI provider.
        
        Returns:
            Current AI provider or None if not set
        """
        return self.current_provider
    
    def get_available_providers(self) -> List[AIProvider]:
        """
        Get list of available AI providers.
        
        Returns:
            List of available AI providers
        """
        return list(self.providers.keys())
    
    def generate_response(self, request: PromptRequest, 
                         provider: Optional[AIProvider] = None) -> AIResponse:
        """
        Generate AI response using the specified or current provider.
        
        Args:
            request: Prompt request
            provider: Specific provider to use (optional)
            
        Returns:
            AI response
        """
        # Use specified provider or current provider
        target_provider = provider or self.current_provider
        
        if not target_provider:
            return self._create_error_response(
                "No AI provider available",
                "NO_PROVIDER",
                request
            )
        
        # Check cache first
        if self.enable_caching:
            cached_response = self._get_cached_response(request, target_provider)
            if cached_response:
                self.logger.debug(f"Returning cached response for {target_provider.value}")
                return cached_response
        
        # Generate response with retries and fallback
        response = self._generate_with_retries(request, target_provider)
        
        # Cache successful responses
        if self.enable_caching and response.success:
            self._cache_response(request, target_provider, response)
        
        # Update statistics
        self._update_provider_stats(target_provider, response)
        
        return response
    
    def _generate_with_retries(self, request: PromptRequest, 
                              provider: AIProvider) -> AIResponse:
        """
        Generate response with retry logic and fallback using error recovery manager.
        
        Args:
            request: Prompt request
            provider: AI provider to use
            
        Returns:
            AI response
        """
        start_time = time.time()
        
        # Get healthy providers from error recovery manager
        all_provider_names = [p.value for p in self.providers.keys()]
        healthy_providers = self.recovery_manager.get_healthy_providers(all_provider_names)
        
        # Ensure primary provider is first if it's healthy
        if provider.value in healthy_providers:
            healthy_providers.remove(provider.value)
            healthy_providers.insert(0, provider.value)
        elif self.recovery_manager.is_provider_available(provider.value):
            healthy_providers.insert(0, provider.value)
        
        last_error = None
        
        for provider_name in healthy_providers:
            # Convert provider name back to enum
            current_provider = None
            for p in self.providers.keys():
                if p.value == provider_name:
                    current_provider = p
                    break
            
            if not current_provider or current_provider not in self.providers:
                continue
            
            # Check if provider is available (circuit breaker not open)
            if not self.recovery_manager.is_provider_available(provider_name):
                self.logger.debug(f"Skipping {provider_name} - circuit breaker is open")
                continue
            
            provider_instance = self.providers[current_provider]
            
            try:
                self.logger.debug(f"Attempting request with {provider_name}")
                
                # Execute with error recovery
                def make_request():
                    return provider_instance.generate_response(request)
                
                response = self.recovery_manager.execute_with_recovery(
                    make_request,
                    provider_name,
                    [p for p in healthy_providers if p != provider_name]
                )
                
                if response and response.success:
                    execution_time = time.time() - start_time
                    self.recovery_manager.record_success(provider_name, execution_time)
                    
                    if current_provider != provider:
                        self.logger.info(f"Fallback to {provider_name} successful")
                    
                    return response
                else:
                    # Handle non-success responses
                    error_msg = response.error_message if response else "Unknown error"
                    error = Exception(error_msg)
                    self.recovery_manager.record_failure(provider_name, error)
                    last_error = response or self._create_error_response(error_msg, "PROVIDER_ERROR", request)
                    
                    # Check if we should continue to next provider
                    if response and response.status in [ResponseStatus.RATE_LIMITED, ResponseStatus.AUTHENTICATION_ERROR]:
                        self.logger.warning(f"Provider {provider_name} returned {response.status}, trying next provider")
                        continue
            
            except Exception as e:
                self.recovery_manager.record_failure(provider_name, e)
                last_error = self._create_error_response(str(e), "PROVIDER_ERROR", request)
                self.logger.warning(f"Provider {provider_name} failed with exception: {e}")
                continue
        
        # All providers failed - return error or fallback response
        if last_error and isinstance(last_error, AIResponse):
            return last_error
        else:
            # Try to get a graceful degradation response
            fallback_content = ErrorHandler.get_fallback_response(
                request.prompt, 
                request.context.get('industry', 'general') if request.context else 'general'
            )
            
            return AIResponse(
                content=fallback_content,
                provider=self.current_provider or AIProvider.OPENAI,
                model="fallback",
                status=ResponseStatus.ERROR,
                error_message="All AI providers failed - using fallback response",
                error_code="ALL_PROVIDERS_FAILED",
                metadata={'request': request.to_dict(), 'fallback': True}
            )
    
    def _get_cached_response(self, request: PromptRequest, 
                           provider: AIProvider) -> Optional[AIResponse]:
        """
        Get cached response if available and not expired.
        
        Args:
            request: Prompt request
            provider: AI provider
            
        Returns:
            Cached response or None
        """
        cache_key = self._generate_cache_key(request, provider)
        
        if cache_key in self.response_cache:
            cached_data = self.response_cache[cache_key]
            
            # Check if cache is still valid
            if datetime.now().timestamp() - cached_data['timestamp'] < self.cache_ttl_seconds:
                # Reconstruct AIResponse from cached data
                return AIResponse(**cached_data['response'])
            else:
                # Remove expired cache entry
                del self.response_cache[cache_key]
        
        return None
    
    def _cache_response(self, request: PromptRequest, provider: AIProvider, 
                       response: AIResponse) -> None:
        """
        Cache the response.
        
        Args:
            request: Prompt request
            provider: AI provider
            response: AI response to cache
        """
        cache_key = self._generate_cache_key(request, provider)
        
        self.response_cache[cache_key] = {
            'timestamp': datetime.now().timestamp(),
            'response': response.to_dict()
        }
        
        # Clean up old cache entries periodically
        if len(self.response_cache) > 1000:  # Arbitrary limit
            self._cleanup_cache()
    
    def _generate_cache_key(self, request: PromptRequest, provider: AIProvider) -> str:
        """
        Generate a cache key for the request.
        
        Args:
            request: Prompt request
            provider: AI provider
            
        Returns:
            Cache key string
        """
        # Create a hash of the request parameters
        request_data = {
            'prompt': request.prompt,
            'context': request.context,
            'system_message': request.system_message,
            'temperature': request.temperature,
            'max_tokens': request.max_tokens,
            'provider': provider.value
        }
        
        request_json = json.dumps(request_data, sort_keys=True)
        return hashlib.md5(request_json.encode()).hexdigest()
    
    def _cleanup_cache(self) -> None:
        """Clean up expired cache entries."""
        current_time = datetime.now().timestamp()
        expired_keys = [
            key for key, data in self.response_cache.items()
            if current_time - data['timestamp'] > self.cache_ttl_seconds
        ]
        
        for key in expired_keys:
            del self.response_cache[key]
        
        self.logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def _update_provider_stats(self, provider: AIProvider, response: AIResponse) -> None:
        """
        Update provider statistics.
        
        Args:
            provider: AI provider
            response: AI response
        """
        if provider not in self.provider_stats:
            return
        
        stats = self.provider_stats[provider]
        stats['requests'] += 1
        stats['last_used'] = datetime.now()
        
        if response.success:
            stats['successes'] += 1
            stats['consecutive_failures'] = 0
        else:
            stats['failures'] += 1
            stats['consecutive_failures'] += 1
        
        if response.response_time:
            stats['total_response_time'] += response.response_time
            stats['average_response_time'] = stats['total_response_time'] / stats['requests']
    
    def _get_provider_success_rate(self, provider: AIProvider) -> float:
        """
        Get the success rate for a provider.
        
        Args:
            provider: AI provider
            
        Returns:
            Success rate (0.0 to 1.0)
        """
        if provider not in self.provider_stats:
            return 0.0
        
        stats = self.provider_stats[provider]
        if stats['requests'] == 0:
            return 0.0
        
        return stats['successes'] / stats['requests']
    
    def _create_error_response(self, message: str, error_code: str, 
                              request: Optional[PromptRequest] = None) -> AIResponse:
        """
        Create a standardized error response.
        
        Args:
            message: Error message
            error_code: Error code
            request: Original request (optional)
            
        Returns:
            Error response
        """
        return AIResponse(
            content="",
            provider=self.current_provider or AIProvider.OPENAI,
            model="orchestrator",
            status=ResponseStatus.ERROR,
            error_message=message,
            error_code=error_code,
            metadata={'request': request.to_dict() if request else None}
        )
    
    def get_provider_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for all providers.
        
        Returns:
            Dictionary of provider statistics
        """
        return {
            provider.value: {
                **stats,
                'success_rate': self._get_provider_success_rate(provider),
                'last_used': stats['last_used'].isoformat() if stats['last_used'] else None
            }
            for provider, stats in self.provider_stats.items()
        }
    
    def get_provider_info(self, provider: Optional[AIProvider] = None) -> Dict[str, Any]:
        """
        Get information about a specific provider or current provider.
        
        Args:
            provider: Specific provider (optional)
            
        Returns:
            Provider information
        """
        target_provider = provider or self.current_provider
        
        if not target_provider or target_provider not in self.providers:
            return {}
        
        provider_instance = self.providers[target_provider]
        model_info = provider_instance.get_model_info()
        
        # Add orchestrator-specific info
        model_info.update({
            'orchestrator_stats': self.provider_stats.get(target_provider, {}),
            'is_current_provider': target_provider == self.current_provider,
            'fallback_available': len(self.providers) > 1
        })
        
        return model_info
    
    def validate_provider_connection(self, provider: Optional[AIProvider] = None) -> bool:
        """
        Validate connection for a specific provider or current provider.
        
        Args:
            provider: Specific provider (optional)
            
        Returns:
            True if connection is valid, False otherwise
        """
        target_provider = provider or self.current_provider
        
        if not target_provider or target_provider not in self.providers:
            return False
        
        try:
            provider_instance = self.providers[target_provider]
            return provider_instance.validate_connection()
        except Exception as e:
            self.logger.error(f"Connection validation failed for {target_provider.value}: {e}")
            return False
    
    def clear_cache(self) -> None:
        """Clear the response cache."""
        self.response_cache.clear()
        self.logger.info("Response cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Cache statistics
        """
        current_time = datetime.now().timestamp()
        valid_entries = sum(
            1 for data in self.response_cache.values()
            if current_time - data['timestamp'] < self.cache_ttl_seconds
        )
        
        return {
            'total_entries': len(self.response_cache),
            'valid_entries': valid_entries,
            'expired_entries': len(self.response_cache) - valid_entries,
            'cache_ttl_seconds': self.cache_ttl_seconds,
            'cache_enabled': self.enable_caching
        }
    
    def __str__(self) -> str:
        """String representation of the orchestrator."""
        return f"AIServiceOrchestrator(providers={len(self.providers)}, current={self.current_provider})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the orchestrator."""
        return (
            f"AIServiceOrchestrator("
            f"providers={list(self.providers.keys())}, "
            f"current={self.current_provider}, "
            f"caching={self.enable_caching}, "
            f"fallback={self.fallback_enabled})"
        )
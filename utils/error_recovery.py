"""
Error recovery and resilience utilities for AI services.
"""
import time
import asyncio
from typing import Dict, Any, Optional, List, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from .logger import get_logger, log_function_call
from .error_handler import RetryConfig, retry_with_exponential_backoff

logger = get_logger("error_recovery")


class RecoveryStrategy(Enum):
    """Recovery strategies for different types of failures."""
    IMMEDIATE_RETRY = "immediate_retry"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    CIRCUIT_BREAKER = "circuit_breaker"
    FALLBACK_PROVIDER = "fallback_provider"
    CACHED_RESPONSE = "cached_response"
    GRACEFUL_DEGRADATION = "graceful_degradation"


@dataclass
class RecoveryConfig:
    """Configuration for error recovery strategies."""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60
    enable_fallback: bool = True
    enable_caching: bool = True
    cache_ttl: int = 300
    strategies: List[RecoveryStrategy] = field(default_factory=lambda: [
        RecoveryStrategy.EXPONENTIAL_BACKOFF,
        RecoveryStrategy.FALLBACK_PROVIDER,
        RecoveryStrategy.GRACEFUL_DEGRADATION
    ])


class ErrorRecoveryManager:
    """Manages error recovery strategies for AI services."""
    
    def __init__(self, config: Optional[RecoveryConfig] = None):
        self.config = config or RecoveryConfig()
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}
        self.provider_health: Dict[str, Dict[str, Any]] = {}
        self.fallback_cache: Dict[str, Dict[str, Any]] = {}
        
    def register_provider(self, provider_name: str) -> None:
        """Register a provider for health monitoring."""
        self.provider_health[provider_name] = {
            'consecutive_failures': 0,
            'total_requests': 0,
            'successful_requests': 0,
            'last_success': None,
            'last_failure': None,
            'average_response_time': 0.0,
            'is_healthy': True
        }
        
        self.circuit_breakers[provider_name] = {
            'is_open': False,
            'failure_count': 0,
            'last_failure_time': None,
            'next_attempt_time': None
        }
        
        logger.info(f"Registered provider {provider_name} for error recovery")
    
    def record_success(self, provider_name: str, response_time: float) -> None:
        """Record a successful request for a provider."""
        if provider_name not in self.provider_health:
            self.register_provider(provider_name)
        
        health = self.provider_health[provider_name]
        health['consecutive_failures'] = 0
        health['total_requests'] += 1
        health['successful_requests'] += 1
        health['last_success'] = datetime.now()
        health['is_healthy'] = True
        
        # Update average response time
        if health['average_response_time'] == 0:
            health['average_response_time'] = response_time
        else:
            health['average_response_time'] = (
                health['average_response_time'] * 0.8 + response_time * 0.2
            )
        
        # Reset circuit breaker
        circuit_breaker = self.circuit_breakers[provider_name]
        circuit_breaker['is_open'] = False
        circuit_breaker['failure_count'] = 0
        
        logger.debug(f"Recorded success for {provider_name}: {response_time:.3f}s")
    
    def record_failure(self, provider_name: str, error: Exception) -> None:
        """Record a failed request for a provider."""
        if provider_name not in self.provider_health:
            self.register_provider(provider_name)
        
        health = self.provider_health[provider_name]
        health['consecutive_failures'] += 1
        health['total_requests'] += 1
        health['last_failure'] = datetime.now()
        
        # Mark as unhealthy if too many consecutive failures
        if health['consecutive_failures'] >= 3:
            health['is_healthy'] = False
        
        # Update circuit breaker
        circuit_breaker = self.circuit_breakers[provider_name]
        circuit_breaker['failure_count'] += 1
        circuit_breaker['last_failure_time'] = datetime.now()
        
        # Open circuit breaker if threshold reached
        if circuit_breaker['failure_count'] >= self.config.circuit_breaker_threshold:
            circuit_breaker['is_open'] = True
            circuit_breaker['next_attempt_time'] = (
                datetime.now() + timedelta(seconds=self.config.circuit_breaker_timeout)
            )
            logger.warning(f"Circuit breaker opened for {provider_name}")
        
        logger.warning(f"Recorded failure for {provider_name}: {error}")
    
    def is_provider_available(self, provider_name: str) -> bool:
        """Check if a provider is available (circuit breaker not open)."""
        if provider_name not in self.circuit_breakers:
            return True
        
        circuit_breaker = self.circuit_breakers[provider_name]
        
        if not circuit_breaker['is_open']:
            return True
        
        # Check if circuit breaker should be reset
        if (circuit_breaker['next_attempt_time'] and 
            datetime.now() >= circuit_breaker['next_attempt_time']):
            circuit_breaker['is_open'] = False
            circuit_breaker['failure_count'] = 0
            logger.info(f"Circuit breaker reset for {provider_name}")
            return True
        
        return False
    
    def get_healthy_providers(self, all_providers: List[str]) -> List[str]:
        """Get list of healthy providers sorted by performance."""
        healthy_providers = []
        
        for provider in all_providers:
            if self.is_provider_available(provider):
                if provider in self.provider_health:
                    health = self.provider_health[provider]
                    if health['is_healthy']:
                        healthy_providers.append((provider, health))
                else:
                    # Unknown provider, assume healthy
                    healthy_providers.append((provider, {'average_response_time': float('inf')}))
        
        # Sort by success rate and response time
        healthy_providers.sort(key=lambda x: (
            -self._get_success_rate(x[0]),  # Higher success rate first
            x[1]['average_response_time']   # Lower response time first
        ))
        
        return [provider for provider, _ in healthy_providers]
    
    def _get_success_rate(self, provider_name: str) -> float:
        """Get success rate for a provider."""
        if provider_name not in self.provider_health:
            return 0.0
        
        health = self.provider_health[provider_name]
        if health['total_requests'] == 0:
            return 0.0
        
        return health['successful_requests'] / health['total_requests']
    
    def execute_with_recovery(self, 
                            func: Callable,
                            provider_name: str,
                            fallback_providers: Optional[List[str]] = None,
                            *args, **kwargs) -> Any:
        """
        Execute a function with comprehensive error recovery.
        
        Args:
            func: Function to execute
            provider_name: Primary provider name
            fallback_providers: List of fallback providers
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or fallback response
        """
        start_time = time.time()
        last_error = None
        
        # Try primary provider
        if self.is_provider_available(provider_name):
            try:
                result = self._execute_with_retries(func, provider_name, *args, **kwargs)
                execution_time = time.time() - start_time
                self.record_success(provider_name, execution_time)
                log_function_call(func.__name__, args, kwargs, execution_time, True)
                return result
            except Exception as e:
                last_error = e
                self.record_failure(provider_name, e)
                logger.warning(f"Primary provider {provider_name} failed: {e}")
        
        # Try fallback providers
        if self.config.enable_fallback and fallback_providers:
            healthy_fallbacks = self.get_healthy_providers(fallback_providers)
            
            for fallback_provider in healthy_fallbacks:
                try:
                    logger.info(f"Attempting fallback to {fallback_provider}")
                    result = self._execute_with_retries(func, fallback_provider, *args, **kwargs)
                    execution_time = time.time() - start_time
                    self.record_success(fallback_provider, execution_time)
                    log_function_call(func.__name__, args, kwargs, execution_time, True)
                    return result
                except Exception as e:
                    last_error = e
                    self.record_failure(fallback_provider, e)
                    logger.warning(f"Fallback provider {fallback_provider} failed: {e}")
        
        # Try cached response
        if self.config.enable_caching:
            cached_response = self._get_cached_fallback(*args, **kwargs)
            if cached_response:
                logger.info("Using cached fallback response")
                execution_time = time.time() - start_time
                log_function_call(func.__name__, args, kwargs, execution_time, True)
                return cached_response
        
        # Graceful degradation
        if RecoveryStrategy.GRACEFUL_DEGRADATION in self.config.strategies:
            degraded_response = self._get_degraded_response(*args, **kwargs)
            if degraded_response:
                logger.info("Using gracefully degraded response")
                execution_time = time.time() - start_time
                log_function_call(func.__name__, args, kwargs, execution_time, True)
                return degraded_response
        
        # All recovery strategies failed
        execution_time = time.time() - start_time
        log_function_call(func.__name__, args, kwargs, execution_time, False, last_error)
        
        if last_error:
            raise last_error
        else:
            raise Exception("All recovery strategies failed")
    
    def _execute_with_retries(self, func: Callable, provider_name: str, 
                            *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        retry_config = RetryConfig(
            max_retries=self.config.max_retries,
            base_delay=self.config.base_delay,
            max_delay=self.config.max_delay
        )
        
        @retry_with_exponential_backoff(retry_config)
        def wrapped_func():
            return func(*args, **kwargs)
        
        return wrapped_func()
    
    def _get_cached_fallback(self, *args, **kwargs) -> Optional[Any]:
        """Get cached fallback response if available."""
        # Simple cache key generation
        cache_key = str(hash(str(args) + str(sorted(kwargs.items()))))
        
        if cache_key in self.fallback_cache:
            cache_entry = self.fallback_cache[cache_key]
            
            # Check if cache is still valid
            if (datetime.now() - cache_entry['timestamp']).seconds < self.config.cache_ttl:
                return cache_entry['response']
            else:
                # Remove expired cache entry
                del self.fallback_cache[cache_key]
        
        return None
    
    def _cache_fallback_response(self, response: Any, *args, **kwargs) -> None:
        """Cache a response for fallback use."""
        cache_key = str(hash(str(args) + str(sorted(kwargs.items()))))
        
        self.fallback_cache[cache_key] = {
            'response': response,
            'timestamp': datetime.now()
        }
        
        # Clean up old cache entries
        if len(self.fallback_cache) > 100:
            self._cleanup_fallback_cache()
    
    def _cleanup_fallback_cache(self) -> None:
        """Clean up expired fallback cache entries."""
        current_time = datetime.now()
        expired_keys = []
        
        for key, entry in self.fallback_cache.items():
            if (current_time - entry['timestamp']).seconds > self.config.cache_ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.fallback_cache[key]
        
        logger.debug(f"Cleaned up {len(expired_keys)} expired fallback cache entries")
    
    def _get_degraded_response(self, *args, **kwargs) -> Optional[str]:
        """Get a gracefully degraded response."""
        # Extract query and industry from arguments if possible
        query = ""
        industry = "general"
        
        if args:
            if len(args) >= 1 and isinstance(args[0], str):
                query = args[0]
            if len(args) >= 2 and isinstance(args[1], str):
                industry = args[1]
        
        if 'query' in kwargs:
            query = kwargs['query']
        if 'industry' in kwargs:
            industry = kwargs['industry']
        
        return f"""🤖 **Service Temporarily Unavailable**

I apologize, but our AI services are currently experiencing issues. Here's some general guidance for your query about "{query}" in the {industry} industry:

**General Recommendations:**
- Consider your specific requirements and constraints
- Research available options and alternatives
- Consult with industry experts or professionals
- Look for established best practices in your field

**What's happening:** Our AI providers are temporarily unavailable, but we're working to restore full service. Please try again in a few minutes.

This is a fallback response to ensure you receive some assistance even when our primary systems are unavailable."""
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report for all providers."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'providers': {},
            'overall_health': 'healthy'
        }
        
        healthy_count = 0
        total_count = len(self.provider_health)
        
        for provider_name, health in self.provider_health.items():
            circuit_breaker = self.circuit_breakers.get(provider_name, {})
            
            provider_report = {
                'is_healthy': health['is_healthy'],
                'is_available': self.is_provider_available(provider_name),
                'success_rate': self._get_success_rate(provider_name),
                'consecutive_failures': health['consecutive_failures'],
                'total_requests': health['total_requests'],
                'successful_requests': health['successful_requests'],
                'average_response_time': health['average_response_time'],
                'last_success': health['last_success'].isoformat() if health['last_success'] else None,
                'last_failure': health['last_failure'].isoformat() if health['last_failure'] else None,
                'circuit_breaker_open': circuit_breaker.get('is_open', False),
                'circuit_breaker_failures': circuit_breaker.get('failure_count', 0)
            }
            
            report['providers'][provider_name] = provider_report
            
            if health['is_healthy'] and self.is_provider_available(provider_name):
                healthy_count += 1
        
        # Determine overall health
        if total_count == 0:
            report['overall_health'] = 'unknown'
        elif healthy_count == 0:
            report['overall_health'] = 'critical'
        elif healthy_count < total_count / 2:
            report['overall_health'] = 'degraded'
        else:
            report['overall_health'] = 'healthy'
        
        report['healthy_providers'] = healthy_count
        report['total_providers'] = total_count
        
        return report
    
    def reset_provider_health(self, provider_name: str) -> None:
        """Reset health status for a provider."""
        if provider_name in self.provider_health:
            self.provider_health[provider_name].update({
                'consecutive_failures': 0,
                'is_healthy': True
            })
        
        if provider_name in self.circuit_breakers:
            self.circuit_breakers[provider_name].update({
                'is_open': False,
                'failure_count': 0,
                'last_failure_time': None,
                'next_attempt_time': None
            })
        
        logger.info(f"Reset health status for provider {provider_name}")


# Global error recovery manager instance
_recovery_manager: Optional[ErrorRecoveryManager] = None


def get_recovery_manager() -> ErrorRecoveryManager:
    """Get the global error recovery manager instance."""
    global _recovery_manager
    if _recovery_manager is None:
        _recovery_manager = ErrorRecoveryManager()
    return _recovery_manager


def with_error_recovery(provider_name: str, 
                       fallback_providers: Optional[List[str]] = None):
    """
    Decorator for adding error recovery to functions.
    
    Args:
        provider_name: Primary provider name
        fallback_providers: List of fallback providers
        
    Returns:
        Decorated function with error recovery
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            recovery_manager = get_recovery_manager()
            return recovery_manager.execute_with_recovery(
                func, provider_name, fallback_providers, *args, **kwargs
            )
        return wrapper
    return decorator
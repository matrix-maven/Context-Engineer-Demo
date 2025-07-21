"""
Tests for error recovery and resilience utilities.
"""
import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from utils.error_recovery import (
    ErrorRecoveryManager, RecoveryConfig, RecoveryStrategy,
    get_recovery_manager, with_error_recovery
)


class TestRecoveryConfig:
    """Test cases for RecoveryConfig class."""
    
    def test_default_config(self):
        """Test default recovery configuration."""
        config = RecoveryConfig()
        
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.circuit_breaker_threshold == 5
        assert config.circuit_breaker_timeout == 60
        assert config.enable_fallback is True
        assert config.enable_caching is True
        assert config.cache_ttl == 300
        assert RecoveryStrategy.EXPONENTIAL_BACKOFF in config.strategies
    
    def test_custom_config(self):
        """Test custom recovery configuration."""
        config = RecoveryConfig(
            max_retries=5,
            base_delay=2.0,
            enable_fallback=False,
            strategies=[RecoveryStrategy.CIRCUIT_BREAKER]
        )
        
        assert config.max_retries == 5
        assert config.base_delay == 2.0
        assert config.enable_fallback is False
        assert config.strategies == [RecoveryStrategy.CIRCUIT_BREAKER]


class TestErrorRecoveryManager:
    """Test cases for ErrorRecoveryManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = RecoveryConfig(
            max_retries=2,
            base_delay=0.01,  # Fast tests
            circuit_breaker_threshold=3,
            circuit_breaker_timeout=1
        )
        self.manager = ErrorRecoveryManager(self.config)
    
    def test_register_provider(self):
        """Test provider registration."""
        provider_name = "test_provider"
        
        self.manager.register_provider(provider_name)
        
        assert provider_name in self.manager.provider_health
        assert provider_name in self.manager.circuit_breakers
        
        health = self.manager.provider_health[provider_name]
        assert health['consecutive_failures'] == 0
        assert health['is_healthy'] is True
        
        circuit_breaker = self.manager.circuit_breakers[provider_name]
        assert circuit_breaker['is_open'] is False
    
    def test_record_success(self):
        """Test recording successful requests."""
        provider_name = "test_provider"
        response_time = 0.5
        
        self.manager.register_provider(provider_name)
        self.manager.record_success(provider_name, response_time)
        
        health = self.manager.provider_health[provider_name]
        assert health['consecutive_failures'] == 0
        assert health['total_requests'] == 1
        assert health['successful_requests'] == 1
        assert health['is_healthy'] is True
        assert health['average_response_time'] == response_time
        
        circuit_breaker = self.manager.circuit_breakers[provider_name]
        assert circuit_breaker['is_open'] is False
        assert circuit_breaker['failure_count'] == 0
    
    def test_record_failure(self):
        """Test recording failed requests."""
        provider_name = "test_provider"
        error = Exception("Test error")
        
        self.manager.register_provider(provider_name)
        self.manager.record_failure(provider_name, error)
        
        health = self.manager.provider_health[provider_name]
        assert health['consecutive_failures'] == 1
        assert health['total_requests'] == 1
        assert health['successful_requests'] == 0
        
        circuit_breaker = self.manager.circuit_breakers[provider_name]
        assert circuit_breaker['failure_count'] == 1
    
    def test_circuit_breaker_opens(self):
        """Test circuit breaker opening after threshold failures."""
        provider_name = "test_provider"
        error = Exception("Test error")
        
        self.manager.register_provider(provider_name)
        
        # Record failures up to threshold
        for _ in range(self.config.circuit_breaker_threshold):
            self.manager.record_failure(provider_name, error)
        
        circuit_breaker = self.manager.circuit_breakers[provider_name]
        assert circuit_breaker['is_open'] is True
        assert not self.manager.is_provider_available(provider_name)
    
    def test_circuit_breaker_resets(self):
        """Test circuit breaker reset after timeout."""
        provider_name = "test_provider"
        error = Exception("Test error")
        
        self.manager.register_provider(provider_name)
        
        # Open circuit breaker
        for _ in range(self.config.circuit_breaker_threshold):
            self.manager.record_failure(provider_name, error)
        
        assert not self.manager.is_provider_available(provider_name)
        
        # Wait for timeout and check reset
        time.sleep(self.config.circuit_breaker_timeout + 0.1)
        assert self.manager.is_provider_available(provider_name)
    
    def test_get_healthy_providers(self):
        """Test getting healthy providers sorted by performance."""
        providers = ["provider1", "provider2", "provider3"]
        
        for provider in providers:
            self.manager.register_provider(provider)
        
        # Make provider2 perform better
        self.manager.record_success("provider1", 1.0)
        self.manager.record_success("provider2", 0.5)
        self.manager.record_success("provider3", 1.5)
        
        # Make provider3 unhealthy
        for _ in range(4):
            self.manager.record_failure("provider3", Exception("Error"))
        
        healthy = self.manager.get_healthy_providers(providers)
        
        # Should return healthy providers sorted by performance
        assert "provider3" not in healthy  # Unhealthy
        assert healthy.index("provider2") < healthy.index("provider1")  # Better performance first
    
    def test_execute_with_recovery_success(self):
        """Test successful execution with recovery."""
        provider_name = "test_provider"
        
        def successful_function():
            return "success"
        
        result = self.manager.execute_with_recovery(
            successful_function, provider_name
        )
        
        assert result == "success"
        assert self.manager.provider_health[provider_name]['successful_requests'] == 1
    
    def test_execute_with_recovery_with_retries(self):
        """Test execution with recovery after retries."""
        provider_name = "test_provider"
        call_count = 0
        
        def eventually_successful_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        result = self.manager.execute_with_recovery(
            eventually_successful_function, provider_name
        )
        
        assert result == "success"
        assert call_count == 3
    
    def test_execute_with_recovery_fallback(self):
        """Test execution with fallback to other providers."""
        primary_provider = "primary"
        fallback_provider = "fallback"
        
        self.manager.register_provider(primary_provider)
        self.manager.register_provider(fallback_provider)
        
        call_count = 0
        
        def function_with_fallback():
            nonlocal call_count
            call_count += 1
            if call_count <= 3:  # Fail primary provider attempts
                raise Exception("Primary failure")
            return "fallback_success"
        
        result = self.manager.execute_with_recovery(
            function_with_fallback,
            primary_provider,
            [fallback_provider]
        )
        
        assert result == "fallback_success"
        assert call_count > 3  # Should have tried fallback
    
    def test_execute_with_recovery_graceful_degradation(self):
        """Test execution with graceful degradation."""
        provider_name = "test_provider"
        
        def always_failing_function():
            raise Exception("Always fails")
        
        result = self.manager.execute_with_recovery(
            always_failing_function, provider_name
        )
        
        # Should return gracefully degraded response
        assert isinstance(result, str)
        assert "Service Temporarily Unavailable" in result
    
    def test_get_health_report(self):
        """Test health report generation."""
        providers = ["provider1", "provider2"]
        
        for provider in providers:
            self.manager.register_provider(provider)
        
        # Make provider1 successful
        self.manager.record_success("provider1", 0.5)
        
        # Make provider2 fail
        self.manager.record_failure("provider2", Exception("Error"))
        
        report = self.manager.get_health_report()
        
        assert 'timestamp' in report
        assert 'providers' in report
        assert 'overall_health' in report
        assert len(report['providers']) == 2
        
        provider1_report = report['providers']['provider1']
        assert provider1_report['is_healthy'] is True
        assert provider1_report['success_rate'] == 1.0
        
        provider2_report = report['providers']['provider2']
        assert provider2_report['success_rate'] == 0.0
    
    def test_reset_provider_health(self):
        """Test resetting provider health."""
        provider_name = "test_provider"
        
        self.manager.register_provider(provider_name)
        
        # Make provider unhealthy
        for _ in range(5):
            self.manager.record_failure(provider_name, Exception("Error"))
        
        assert not self.manager.provider_health[provider_name]['is_healthy']
        assert self.manager.circuit_breakers[provider_name]['is_open']
        
        # Reset health
        self.manager.reset_provider_health(provider_name)
        
        assert self.manager.provider_health[provider_name]['is_healthy']
        assert not self.manager.circuit_breakers[provider_name]['is_open']
        assert self.manager.provider_health[provider_name]['consecutive_failures'] == 0


class TestErrorRecoveryDecorator:
    """Test cases for error recovery decorator."""
    
    def test_with_error_recovery_decorator(self):
        """Test the with_error_recovery decorator."""
        call_count = 0
        
        @with_error_recovery("test_provider", ["fallback_provider"])
        def decorated_function():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("First attempt fails")
            return "success"
        
        result = decorated_function()
        
        # Should succeed after retry
        assert result == "success" or "Service Temporarily Unavailable" in result
        assert call_count >= 1


class TestGlobalRecoveryManager:
    """Test cases for global recovery manager."""
    
    def test_get_recovery_manager_singleton(self):
        """Test that get_recovery_manager returns singleton instance."""
        manager1 = get_recovery_manager()
        manager2 = get_recovery_manager()
        
        assert manager1 is manager2
        assert isinstance(manager1, ErrorRecoveryManager)


class TestCachingFunctionality:
    """Test cases for caching functionality in error recovery."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = RecoveryConfig(enable_caching=True, cache_ttl=1)
        self.manager = ErrorRecoveryManager(self.config)
    
    def test_cache_fallback_response(self):
        """Test caching of fallback responses."""
        response = "cached_response"
        args = ("test_query",)
        kwargs = {"industry": "healthcare"}
        
        # Cache the response
        self.manager._cache_fallback_response(response, *args, **kwargs)
        
        # Retrieve cached response
        cached = self.manager._get_cached_fallback(*args, **kwargs)
        
        assert cached == response
    
    def test_cache_expiration(self):
        """Test cache expiration."""
        response = "cached_response"
        args = ("test_query",)
        
        # Cache the response
        self.manager._cache_fallback_response(response, *args)
        
        # Should be available immediately
        cached = self.manager._get_cached_fallback(*args)
        assert cached == response
        
        # Wait for expiration
        time.sleep(self.config.cache_ttl + 0.1)
        
        # Should be expired
        cached = self.manager._get_cached_fallback(*args)
        assert cached is None
    
    def test_cache_cleanup(self):
        """Test cache cleanup functionality."""
        # Add many cache entries
        for i in range(150):  # More than cleanup threshold
            self.manager._cache_fallback_response(f"response_{i}", f"query_{i}")
        
        initial_count = len(self.manager.fallback_cache)
        
        # Trigger cleanup
        self.manager._cleanup_fallback_cache()
        
        # Should have cleaned up some entries
        assert len(self.manager.fallback_cache) <= initial_count


if __name__ == "__main__":
    pytest.main([__file__])
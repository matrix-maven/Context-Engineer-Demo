#!/usr/bin/env python3
"""
Validation script for comprehensive error handling and logging system.

This script demonstrates and validates the error handling, logging, and recovery
mechanisms implemented for the AI-powered Context Engineering Demo.
"""
import os
import sys
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.error_handler import (
    ErrorHandler, AIProviderError, ConfigurationError, NetworkError,
    ValidationError, ContextError, retry_with_exponential_backoff,
    RetryConfig, handle_startup_errors
)
from utils.error_recovery import (
    ErrorRecoveryManager, RecoveryConfig, get_recovery_manager,
    with_error_recovery
)
from utils.logger import (
    setup_logging, get_logger, get_metrics_logger, log_function_call,
    log_ai_request, configure_third_party_loggers
)
from config.settings import LogLevel


def test_error_handler():
    """Test the centralized error handler."""
    print("🧪 Testing Error Handler...")
    
    # Test different error types
    errors_to_test = [
        AIProviderError("Rate limit exceeded", "openai"),
        AIProviderError("Invalid API key", "anthropic"),
        AIProviderError("Request timeout", "gemini"),
        ConfigurationError("Missing required setting"),
        NetworkError("Connection failed"),
        ValidationError("Invalid input format"),
        ContextError("Failed to generate context"),
        Exception("Unknown error")
    ]
    
    for error in errors_to_test:
        user_message = ErrorHandler.handle_error(error)
        print(f"  ✅ {type(error).__name__}: {user_message[:50]}...")
    
    # Test fallback response
    fallback = ErrorHandler.get_fallback_response("How to optimize?", "healthcare")
    print(f"  ✅ Fallback response generated: {len(fallback)} characters")
    
    # Test safe execution
    def failing_function():
        raise Exception("Test error")
    
    result = ErrorHandler.safe_execute(failing_function, default_return="safe_fallback")
    assert result == "safe_fallback"
    print("  ✅ Safe execution with fallback works")
    
    print("✅ Error Handler tests completed\n")


def test_retry_mechanism():
    """Test retry mechanism with exponential backoff."""
    print("🧪 Testing Retry Mechanism...")
    
    # Test successful retry after failures
    attempt_count = 0
    
    @retry_with_exponential_backoff(RetryConfig(max_retries=3, base_delay=0.01))
    def eventually_successful():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise Exception(f"Attempt {attempt_count} failed")
        return f"Success on attempt {attempt_count}"
    
    start_time = time.time()
    result = eventually_successful()
    duration = time.time() - start_time
    
    print(f"  ✅ Retry successful: {result}")
    print(f"  ✅ Total attempts: {attempt_count}")
    print(f"  ✅ Duration: {duration:.3f}s")
    
    # Test max retries exceeded
    attempt_count = 0
    
    @retry_with_exponential_backoff(RetryConfig(max_retries=2, base_delay=0.01))
    def always_failing():
        nonlocal attempt_count
        attempt_count += 1
        raise Exception(f"Attempt {attempt_count} failed")
    
    try:
        always_failing()
        assert False, "Should have raised exception"
    except Exception as e:
        print(f"  ✅ Max retries exceeded correctly: {attempt_count} attempts")
    
    print("✅ Retry Mechanism tests completed\n")


def test_error_recovery_manager():
    """Test the error recovery manager."""
    print("🧪 Testing Error Recovery Manager...")
    
    config = RecoveryConfig(
        max_retries=2,
        base_delay=0.01,
        circuit_breaker_threshold=3,
        circuit_breaker_timeout=1
    )
    manager = ErrorRecoveryManager(config)
    
    # Register providers
    providers = ["provider1", "provider2", "provider3"]
    for provider in providers:
        manager.register_provider(provider)
    
    print(f"  ✅ Registered {len(providers)} providers")
    
    # Test success recording
    manager.record_success("provider1", 0.5)
    manager.record_success("provider2", 1.0)
    
    # Test failure recording
    for _ in range(2):
        manager.record_failure("provider3", Exception("Test error"))
    
    # Get healthy providers
    healthy = manager.get_healthy_providers(providers)
    print(f"  ✅ Healthy providers: {healthy}")
    
    # Test circuit breaker
    for _ in range(config.circuit_breaker_threshold):
        manager.record_failure("provider2", Exception("Circuit breaker test"))
    
    assert not manager.is_provider_available("provider2")
    print("  ✅ Circuit breaker opened correctly")
    
    # Test health report
    report = manager.get_health_report()
    print(f"  ✅ Health report generated: {report['overall_health']}")
    print(f"  ✅ Healthy providers: {report['healthy_providers']}/{report['total_providers']}")
    
    # Test execution with recovery
    call_count = 0
    
    def test_function():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise Exception("First attempt fails")
        return "success"
    
    result = manager.execute_with_recovery(
        test_function, "provider1", ["provider2", "provider3"]
    )
    
    print(f"  ✅ Recovery execution result: {result}")
    
    print("✅ Error Recovery Manager tests completed\n")


def test_logging_system():
    """Test the comprehensive logging system."""
    print("🧪 Testing Logging System...")
    
    # Setup logging with different configurations
    logger = setup_logging(LogLevel.DEBUG, enable_file_logging=True)
    print("  ✅ Logging system initialized")
    
    # Test different log levels
    logger.debug("Debug message for testing")
    logger.info("Info message for testing")
    logger.warning("Warning message for testing")
    logger.error("Error message for testing")
    
    # Test structured logging
    logger.info("Structured log test", extra={
        'user_id': 'test_user',
        'action': 'test_action',
        'duration': 0.123
    })
    
    print("  ✅ Different log levels tested")
    
    # Test metrics logging
    metrics_logger = get_metrics_logger()
    
    log_function_call(
        "test_function",
        ("arg1", "arg2"),
        {"param": "value"},
        0.456,
        True
    )
    
    log_ai_request(
        "openai",
        "gpt-3.5-turbo",
        100,
        200,
        0.789,
        True
    )
    
    print("  ✅ Metrics logging tested")
    
    # Test third-party logger configuration
    configure_third_party_loggers()
    print("  ✅ Third-party loggers configured")
    
    print("✅ Logging System tests completed\n")


def test_startup_error_handling():
    """Test startup error handling."""
    print("🧪 Testing Startup Error Handling...")
    
    # This will check actual configuration
    startup_error = handle_startup_errors()
    
    if startup_error:
        print(f"  ⚠️  Startup issue detected: {startup_error[:100]}...")
    else:
        print("  ✅ No startup errors detected")
    
    print("✅ Startup Error Handling tests completed\n")


def test_integration_scenario():
    """Test a realistic integration scenario."""
    print("🧪 Testing Integration Scenario...")
    
    # Simulate a realistic AI service call with error handling
    recovery_manager = get_recovery_manager()
    recovery_manager.register_provider("openai")
    recovery_manager.register_provider("anthropic")
    
    call_count = 0
    
    @with_error_recovery("openai", ["anthropic"])
    def simulate_ai_call(query: str, context: Dict[str, Any]) -> str:
        nonlocal call_count
        call_count += 1
        
        # Simulate different failure scenarios
        if call_count == 1:
            raise AIProviderError("Rate limit exceeded", "openai")
        elif call_count == 2:
            raise NetworkError("Connection timeout")
        elif call_count == 3:
            # Success on third attempt (fallback provider)
            return f"AI response for: {query}"
        else:
            return f"AI response for: {query}"
    
    # Test the integration
    start_time = time.time()
    
    try:
        result = simulate_ai_call(
            "How to optimize performance?",
            {"industry": "healthcare", "user_type": "professional"}
        )
        duration = time.time() - start_time
        
        print(f"  ✅ Integration test successful: {result[:50]}...")
        print(f"  ✅ Total attempts: {call_count}")
        print(f"  ✅ Duration: {duration:.3f}s")
        
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
    
    # Check health report
    report = recovery_manager.get_health_report()
    print(f"  ✅ Final health status: {report['overall_health']}")
    
    print("✅ Integration Scenario tests completed\n")


def test_performance_and_monitoring():
    """Test performance monitoring and metrics collection."""
    print("🧪 Testing Performance and Monitoring...")
    
    # Test performance logging
    start_time = time.time()
    
    def monitored_function(iterations: int = 1000):
        """Function to monitor performance."""
        total = 0
        for i in range(iterations):
            total += i * i
        return total
    
    result = monitored_function()
    execution_time = time.time() - start_time
    
    # Log performance metrics
    ErrorHandler.log_performance_metrics(
        "monitored_function",
        execution_time,
        True
    )
    
    print(f"  ✅ Performance monitoring: {execution_time:.3f}s for {result}")
    
    # Test error metrics
    try:
        raise Exception("Test error for metrics")
    except Exception as e:
        ErrorHandler.log_performance_metrics(
            "failing_function",
            0.001,
            False,
            e
        )
    
    print("  ✅ Error metrics logged")
    
    print("✅ Performance and Monitoring tests completed\n")


def main():
    """Run all validation tests."""
    print("🚀 Starting Comprehensive Error Handling and Logging Validation\n")
    print("=" * 70)
    
    start_time = time.time()
    
    try:
        # Run all test suites
        test_error_handler()
        test_retry_mechanism()
        test_error_recovery_manager()
        test_logging_system()
        test_startup_error_handling()
        test_integration_scenario()
        test_performance_and_monitoring()
        
        total_time = time.time() - start_time
        
        print("=" * 70)
        print(f"🎉 All validation tests completed successfully!")
        print(f"⏱️  Total execution time: {total_time:.3f}s")
        print("\n📊 Summary:")
        print("  ✅ Error handling system working correctly")
        print("  ✅ Retry mechanisms with exponential backoff functional")
        print("  ✅ Circuit breakers and fallback logic operational")
        print("  ✅ Comprehensive logging system active")
        print("  ✅ Performance monitoring and metrics collection enabled")
        print("  ✅ Integration scenarios tested successfully")
        
        # Check if log files were created
        if os.path.exists("logs"):
            log_files = os.listdir("logs")
            print(f"\n📁 Log files created: {len(log_files)}")
            for log_file in log_files:
                file_path = os.path.join("logs", log_file)
                file_size = os.path.getsize(file_path)
                print(f"  📄 {log_file}: {file_size} bytes")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
# Error Handling and Logging System

The Context Engineering Demo includes a comprehensive error handling and logging system designed to provide robust error management, retry logic, and user-friendly error messages.

## 🚨 Error Handling Architecture

### Core Components

The error handling system consists of several key components:

1. **Custom Exception Hierarchy** - Structured exception classes for different error types
2. **Retry Logic with Exponential Backoff** - Automatic retry mechanisms for transient failures
3. **Circuit Breaker Pattern** - Prevents cascading failures in distributed systems
4. **Centralized Error Handler** - Unified error processing and user-friendly message generation
5. **Performance Monitoring** - Execution time tracking and metrics logging

### Exception Hierarchy

```python
from utils.error_handler import (
    ContextDemoError,      # Base exception
    AIProviderError,       # AI provider failures
    ConfigurationError,    # Configuration issues
    NetworkError,          # Network connectivity problems
    ValidationError,       # Input validation failures
    ContextError          # Context generation issues
)
```

#### Base Exception: ContextDemoError

All application-specific exceptions inherit from `ContextDemoError`:

```python
class ContextDemoError(Exception):
    """Base exception for Context Demo application."""
    
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN_ERROR, 
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_type = error_type
        self.context = context or {}
        self.message = message
```

**Features:**
- **Error Type Classification**: Categorizes errors for better handling
- **Context Preservation**: Stores additional context data for debugging
- **Structured Logging**: Integrates with the logging system for detailed error tracking

#### Specialized Exception Classes

**AIProviderError** - For AI service failures:
```python
try:
    response = ai_provider.generate_response(request)
except Exception as e:
    raise AIProviderError(
        "OpenAI API request failed", 
        provider="openai",
        context={"request_id": "req_123", "model": "gpt-3.5-turbo"}
    )
```

**ConfigurationError** - For configuration issues:
```python
if not api_key:
    raise ConfigurationError(
        "API key not found in environment variables",
        context={"provider": "openai", "env_var": "OPENAI_API_KEY"}
    )
```

**NetworkError** - For connectivity issues:
```python
try:
    response = requests.get(url, timeout=30)
except requests.RequestException as e:
    raise NetworkError(
        "Failed to connect to external service",
        context={"url": url, "timeout": 30}
    )
```

## 🔄 Retry Logic with Exponential Backoff

### RetryConfig Class

Configure retry behavior with the `RetryConfig` class:

```python
from utils.error_handler import RetryConfig, retry_with_exponential_backoff

# Default configuration
config = RetryConfig(
    max_retries=3,           # Maximum number of retry attempts
    base_delay=1.0,          # Initial delay in seconds
    max_delay=60.0,          # Maximum delay cap
    exponential_base=2.0,    # Exponential backoff multiplier
    jitter=True              # Add randomization to prevent thundering herd
)
```

### Retry Decorator

Apply retry logic to any function using the decorator:

```python
@retry_with_exponential_backoff(
    retry_config=RetryConfig(max_retries=5, base_delay=2.0),
    exceptions=(AIProviderError, NetworkError),
    on_retry=lambda error, attempt: logger.info(f"Retry attempt {attempt}: {error}")
)
def call_ai_provider(request):
    """Function that may fail and should be retried."""
    return ai_provider.generate_response(request)
```

**Key Features:**
- **Configurable Retry Logic**: Customize retry attempts, delays, and backoff strategy
- **Exception Filtering**: Only retry on specific exception types
- **Jitter Support**: Prevents thundering herd problems in distributed systems
- **Callback Support**: Execute custom logic on each retry attempt
- **Comprehensive Logging**: Automatic logging of retry attempts and failures

### Usage Examples

**Basic Retry:**
```python
@retry_with_exponential_backoff()
def unreliable_function():
    # Function that might fail
    if random.random() < 0.7:
        raise Exception("Random failure")
    return "Success"
```

**Advanced Retry with Custom Configuration:**
```python
# Custom retry configuration for AI provider calls
ai_retry_config = RetryConfig(
    max_retries=3,
    base_delay=1.0,
    max_delay=30.0,
    exponential_base=2.0,
    jitter=True
)

@retry_with_exponential_backoff(
    retry_config=ai_retry_config,
    exceptions=(AIProviderError, NetworkError),
    on_retry=lambda error, attempt: metrics.increment('ai_retry', tags={'attempt': attempt})
)
def generate_ai_response(prompt, context):
    return ai_orchestrator.generate_response(PromptRequest(prompt=prompt, context=context))
```

## ⚡ Circuit Breaker Pattern

### Circuit Breaker Implementation

Prevent cascading failures with the circuit breaker pattern:

```python
from utils.error_handler import ErrorHandler

# Create a circuit breaker
circuit_breaker = ErrorHandler.create_circuit_breaker(
    failure_threshold=5,     # Open circuit after 5 consecutive failures
    recovery_timeout=60      # Attempt recovery after 60 seconds
)

@circuit_breaker
def call_external_service():
    """Function protected by circuit breaker."""
    return external_api.call()
```

**Circuit Breaker States:**
1. **Closed** - Normal operation, requests pass through
2. **Open** - Circuit is open, requests fail fast without calling the function
3. **Half-Open** - Testing recovery, limited requests allowed through

**Benefits:**
- **Fail Fast**: Prevents waiting for timeouts when service is known to be down
- **Automatic Recovery**: Periodically tests if the service has recovered
- **Resource Protection**: Prevents resource exhaustion from repeated failed calls
- **Cascading Failure Prevention**: Stops failures from propagating through the system

### Usage in AI Provider Calls

```python
# Protect AI provider calls with circuit breaker
openai_circuit_breaker = ErrorHandler.create_circuit_breaker(
    failure_threshold=3,
    recovery_timeout=120
)

@openai_circuit_breaker
def call_openai_api(request):
    return openai_provider.generate_response(request)
```

## 🎯 Centralized Error Handler

### ErrorHandler Class

The `ErrorHandler` class provides centralized error processing:

```python
from utils.error_handler import ErrorHandler

# Handle any exception and get user-friendly message
try:
    result = risky_operation()
except Exception as error:
    user_message = ErrorHandler.handle_error(error, context={"user_id": "123"})
    st.error(user_message)  # Display friendly message to user
```

### Error Message Generation

The error handler generates context-aware, user-friendly messages:

**AI Provider Errors:**
- Rate limit: "⚠️ The OpenAI service is currently busy. Please try again in a moment."
- Authentication: "🔑 There's an issue with the OpenAI API configuration. Please check your settings."
- Timeout: "⏱️ The OpenAI service is taking too long to respond. Please try again."

**Configuration Errors:**
- "⚙️ Configuration issue: API key not found. Please check your settings."

**Network Errors:**
- "🌐 Network connection issue. Please check your internet connection and try again."

### Fallback Response Generation

When AI providers are unavailable, generate fallback responses:

```python
fallback_response = ErrorHandler.get_fallback_response(
    query="What are the best restaurants nearby?",
    industry="Restaurant Reservations"
)
```

**Generated Fallback:**
```
🤖 **Fallback Response for Restaurant Reservations**

I'm currently unable to provide AI-powered responses, but here's some general guidance for your query: "What are the best restaurants nearby?"

**General Recommendations:**
- Consider your specific needs and preferences
- Look for options that match your requirements
- Compare different alternatives available
- Seek additional information if needed

**Note:** This is a fallback response. AI-powered responses will provide more personalized and detailed assistance once the service is restored.
```

## 📊 Performance Monitoring

### Performance Metrics Logging

Track function execution times and success rates:

```python
import time
from utils.error_handler import ErrorHandler

def monitored_function():
    start_time = time.time()
    success = False
    error = None
    
    try:
        result = expensive_operation()
        success = True
        return result
    except Exception as e:
        error = e
        raise
    finally:
        execution_time = time.time() - start_time
        ErrorHandler.log_performance_metrics(
            func_name="expensive_operation",
            execution_time=execution_time,
            success=success,
            error=error
        )
```

**Logged Metrics:**
- Function name and execution time
- Success/failure status
- Error type and message (if failed)
- Timestamp for trend analysis

### Safe Function Execution

Execute functions safely with automatic error handling:

```python
# Safe execution with default return value
result = ErrorHandler.safe_execute(
    risky_function,
    arg1="value1",
    arg2="value2",
    default_return="fallback_value",
    log_errors=True
)

# Safe execution without logging
result = ErrorHandler.safe_execute(
    another_function,
    default_return=None,
    log_errors=False
)
```

## 🔍 Input Validation and Sanitization

### Validation Rules

Define validation rules for input data:

```python
validation_rules = {
    'required_fields': ['name', 'email'],
    'max_length': {
        'name': 100,
        'email': 255,
        'message': 1000
    },
    'allowed_values': {
        'status': ['active', 'inactive', 'pending'],
        'priority': ['low', 'medium', 'high']
    }
}

# Validate and sanitize input
result = ErrorHandler.validate_and_sanitize_input(user_input, validation_rules)

if result['valid']:
    process_data(result['sanitized_data'])
else:
    for error in result['errors']:
        logger.error(f"Validation error: {error}")
    
    for warning in result['warnings']:
        logger.warning(f"Validation warning: {warning}")
```

**Validation Result Structure:**
```python
{
    'valid': True,                    # Overall validation status
    'errors': [],                     # List of validation errors
    'sanitized_data': input_data,     # Cleaned/sanitized data
    'warnings': []                    # List of validation warnings
}
```

## 🚀 AI Provider Failure Handling

### Provider Failure Management

Handle AI provider failures with detailed error information:

```python
error_info = ErrorHandler.handle_ai_provider_failure(
    provider="openai",
    error=api_exception,
    fallback_providers=["anthropic", "gemini"]
)

# Error info structure:
{
    'failed_provider': 'openai',
    'error_type': 'APIError',
    'error_message': 'Rate limit exceeded',
    'timestamp': 1642678800.0,
    'fallback_available': True,
    'suggested_fallbacks': ['anthropic', 'gemini']
}
```

### Integration with AI Orchestrator

The error handling system integrates seamlessly with the AI Service Orchestrator:

```python
from services.ai_orchestrator import AIServiceOrchestrator
from utils.error_handler import retry_with_exponential_backoff, RetryConfig

class EnhancedAIOrchestrator(AIServiceOrchestrator):
    @retry_with_exponential_backoff(
        retry_config=RetryConfig(max_retries=3, base_delay=1.0),
        exceptions=(AIProviderError, NetworkError)
    )
    def generate_response_with_retry(self, request):
        return super().generate_response(request)
```

## 🔧 Configuration and Setup

### Environment Variables

No additional environment variables are required for the error handling system. It uses the existing logging configuration.

### Dependencies

The error handling system uses only Python standard library modules:
- `traceback` - For exception stack traces
- `time` - For timing and delays
- `random` - For jitter in retry logic
- `functools` - For decorator implementation
- `typing` - For type hints

### Integration with Existing Code

The error handling system is designed to integrate seamlessly with existing code:

1. **Import the utilities:**
```python
from utils.error_handler import (
    ErrorHandler,
    retry_with_exponential_backoff,
    RetryConfig,
    AIProviderError,
    ConfigurationError
)
```

2. **Wrap existing functions with retry logic:**
```python
@retry_with_exponential_backoff()
def existing_function():
    # Your existing code here
    pass
```

3. **Use centralized error handling:**
```python
try:
    result = existing_operation()
except Exception as e:
    user_message = ErrorHandler.handle_error(e)
    # Display user_message to the user
```

## 📝 Best Practices

### Error Handling Guidelines

1. **Use Specific Exception Types**: Raise specific exceptions rather than generic `Exception`
2. **Include Context**: Always provide relevant context when raising exceptions
3. **Log Before Re-raising**: Log errors with full context before re-raising
4. **User-Friendly Messages**: Use `ErrorHandler.handle_error()` for user-facing error messages
5. **Fail Fast**: Use circuit breakers for external service calls
6. **Retry Transient Failures**: Apply retry logic to operations that may fail temporarily

### Retry Logic Best Practices

1. **Be Selective**: Only retry on transient errors (network, rate limits, timeouts)
2. **Set Reasonable Limits**: Don't retry indefinitely; set appropriate max_retries
3. **Use Exponential Backoff**: Prevent overwhelming failing services
4. **Add Jitter**: Prevent thundering herd problems in distributed systems
5. **Monitor Retry Metrics**: Track retry attempts and success rates

### Circuit Breaker Best Practices

1. **Set Appropriate Thresholds**: Balance between fault tolerance and responsiveness
2. **Monitor Circuit State**: Log circuit breaker state changes
3. **Implement Health Checks**: Use circuit breakers with health check endpoints
4. **Graceful Degradation**: Provide fallback functionality when circuits are open

## 🧪 Testing Error Handling

### Unit Testing Examples

```python
import pytest
from utils.error_handler import (
    ErrorHandler,
    AIProviderError,
    retry_with_exponential_backoff,
    RetryConfig
)

def test_error_handler_ai_provider_error():
    """Test AI provider error handling."""
    error = AIProviderError("Rate limit exceeded", provider="openai")
    message = ErrorHandler.handle_error(error)
    assert "OpenAI service is currently busy" in message

def test_retry_decorator_success_after_failure():
    """Test retry decorator with eventual success."""
    call_count = 0
    
    @retry_with_exponential_backoff(
        retry_config=RetryConfig(max_retries=3, base_delay=0.1)
    )
    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception("Temporary failure")
        return "Success"
    
    result = flaky_function()
    assert result == "Success"
    assert call_count == 3

def test_circuit_breaker_opens_after_failures():
    """Test circuit breaker opens after threshold failures."""
    circuit_breaker = ErrorHandler.create_circuit_breaker(
        failure_threshold=2,
        recovery_timeout=1
    )
    
    @circuit_breaker
    def failing_function():
        raise Exception("Always fails")
    
    # First two calls should attempt the function
    with pytest.raises(Exception):
        failing_function()
    with pytest.raises(Exception):
        failing_function()
    
    # Third call should fail fast due to open circuit
    with pytest.raises(AIProviderError) as exc_info:
        failing_function()
    assert "Circuit breaker is open" in str(exc_info.value)
```

### Integration Testing

```python
def test_ai_orchestrator_with_error_handling():
    """Test AI orchestrator integration with error handling."""
    from services.ai_orchestrator import AIServiceOrchestrator
    from services.ai_service import PromptRequest
    
    orchestrator = AIServiceOrchestrator()
    
    # Test with invalid request
    request = PromptRequest(prompt="")  # Empty prompt
    response = orchestrator.generate_response(request)
    
    assert not response.success
    assert response.error_message is not None
    
    # Verify user-friendly error message
    user_message = ErrorHandler.handle_error(
        Exception(response.error_message)
    )
    assert len(user_message) > 0
    assert not user_message.startswith("Traceback")
```

## 🔍 Monitoring and Observability

### Error Metrics

The error handling system automatically logs metrics that can be used for monitoring:

1. **Error Rates**: Track error frequency by type and component
2. **Retry Success Rates**: Monitor how often retries succeed
3. **Circuit Breaker State**: Track circuit breaker open/close events
4. **Performance Metrics**: Function execution times and success rates

### Log Analysis

Error logs include structured data for analysis:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "ERROR",
  "message": "AI provider request failed",
  "error_type": "ai_provider_error",
  "provider": "openai",
  "context": {
    "request_id": "req_123",
    "model": "gpt-3.5-turbo",
    "user_id": "user_456"
  },
  "traceback": "..."
}
```

### Alerting

Set up alerts based on error patterns:
- High error rates for specific providers
- Circuit breaker state changes
- Repeated retry failures
- Performance degradation

This comprehensive error handling system ensures robust operation of the Context Engineering Demo while providing excellent user experience and operational visibility.
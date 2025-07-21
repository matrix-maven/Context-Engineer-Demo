"""
Logging configuration and utilities.
"""
import logging
import logging.handlers
import sys
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from config.settings import get_settings, LogLevel


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra') and record.extra:
            log_entry.update(record.extra)
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, default=str)


class ColoredConsoleFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format the message
        formatted = super().format(record)
        
        # Add color to level name
        formatted = formatted.replace(
            record.levelname,
            f"{color}{record.levelname}{reset}"
        )
        
        return formatted


def setup_logging(log_level: Optional[LogLevel] = None, 
                 enable_file_logging: bool = True,
                 enable_structured_logging: bool = False) -> logging.Logger:
    """
    Set up comprehensive application logging configuration.
    
    Args:
        log_level: Logging level to use
        enable_file_logging: Whether to enable file logging
        enable_structured_logging: Whether to use structured JSON logging
        
    Returns:
        Configured application logger
    """
    settings = get_settings()
    
    # Use provided log level or default from settings
    level = log_level or settings.log_level
    log_level_int = getattr(logging, level.value)
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    if enable_file_logging:
        log_dir.mkdir(exist_ok=True)
    
    # Clear any existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Set root logger level
    root_logger.setLevel(log_level_int)
    
    handlers = []
    
    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level_int)
    
    if enable_structured_logging:
        console_formatter = StructuredFormatter()
    else:
        console_formatter = ColoredConsoleFormatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)
    
    # File handlers
    if enable_file_logging:
        # General application log
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "context_demo.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)-30s | %(funcName)-20s:%(lineno)-4d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
        
        # Error-only log
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "errors.log",
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        handlers.append(error_handler)
        
        # Performance metrics log
        metrics_handler = logging.handlers.RotatingFileHandler(
            log_dir / "metrics.log",
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3
        )
        metrics_handler.setLevel(logging.INFO)
        
        # Use structured format for metrics
        metrics_formatter = StructuredFormatter()
        metrics_handler.setFormatter(metrics_formatter)
        
        # Create metrics logger
        metrics_logger = logging.getLogger("context_demo.metrics")
        metrics_logger.addHandler(metrics_handler)
        metrics_logger.setLevel(logging.INFO)
        metrics_logger.propagate = False
    
    # Add all handlers to root logger
    for handler in handlers:
        root_logger.addHandler(handler)
    
    # Create application logger
    logger = logging.getLogger("context_demo")
    logger.setLevel(log_level_int)
    
    # Log startup message
    logger.info(f"Logging initialized with level: {level.value}")
    if enable_file_logging:
        logger.info(f"Log files will be written to: {log_dir.absolute()}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name for the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"context_demo.{name}")


def get_metrics_logger() -> logging.Logger:
    """
    Get the metrics logger for performance tracking.
    
    Returns:
        Metrics logger instance
    """
    return logging.getLogger("context_demo.metrics")


def log_function_call(func_name: str, args: tuple = (), kwargs: dict = None, 
                     execution_time: Optional[float] = None,
                     success: bool = True, error: Optional[Exception] = None) -> None:
    """
    Log function call details for debugging and monitoring.
    
    Args:
        func_name: Name of the function
        args: Function arguments
        kwargs: Function keyword arguments
        execution_time: Time taken to execute
        success: Whether the function succeeded
        error: Exception if function failed
    """
    metrics_logger = get_metrics_logger()
    
    log_data = {
        'event_type': 'function_call',
        'function': func_name,
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if execution_time is not None:
        log_data['execution_time'] = execution_time
    
    if args:
        # Don't log sensitive data
        safe_args = [str(arg)[:100] if isinstance(arg, str) else type(arg).__name__ for arg in args]
        log_data['args_count'] = len(args)
        log_data['args_types'] = safe_args
    
    if kwargs:
        # Don't log sensitive data
        safe_kwargs = {k: str(v)[:100] if isinstance(v, str) else type(v).__name__ 
                      for k, v in (kwargs or {}).items()}
        log_data['kwargs'] = safe_kwargs
    
    if error:
        log_data['error_type'] = type(error).__name__
        log_data['error_message'] = str(error)[:500]  # Truncate long error messages
    
    if success:
        metrics_logger.info("Function call completed", extra=log_data)
    else:
        metrics_logger.warning("Function call failed", extra=log_data)


def log_ai_request(provider: str, model: str, prompt_length: int, 
                  response_length: Optional[int] = None,
                  execution_time: Optional[float] = None,
                  success: bool = True, error: Optional[str] = None) -> None:
    """
    Log AI API request details for monitoring and debugging.
    
    Args:
        provider: AI provider name
        model: Model used
        prompt_length: Length of the prompt
        response_length: Length of the response
        execution_time: Time taken for the request
        success: Whether the request succeeded
        error: Error message if request failed
    """
    metrics_logger = get_metrics_logger()
    
    log_data = {
        'event_type': 'ai_request',
        'provider': provider,
        'model': model,
        'prompt_length': prompt_length,
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if response_length is not None:
        log_data['response_length'] = response_length
    
    if execution_time is not None:
        log_data['execution_time'] = execution_time
    
    if error:
        log_data['error'] = error[:500]  # Truncate long error messages
    
    if success:
        metrics_logger.info("AI request completed", extra=log_data)
    else:
        metrics_logger.warning("AI request failed", extra=log_data)


def configure_third_party_loggers() -> None:
    """Configure logging levels for third-party libraries."""
    # Reduce noise from third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    logging.getLogger("streamlit").setLevel(logging.WARNING)


# Global logger instance
_logger: Optional[logging.Logger] = None


def get_app_logger() -> logging.Logger:
    """
    Get the main application logger.
    
    Returns:
        Main application logger
    """
    global _logger
    if _logger is None:
        _logger = setup_logging()
        configure_third_party_loggers()
    return _logger


def shutdown_logging() -> None:
    """Properly shutdown logging handlers."""
    logging.shutdown()
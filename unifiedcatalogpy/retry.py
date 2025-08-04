"""
Retry logic and reliability utilities for UnifiedCatalogPy.
"""

import time
import random
from typing import Callable, Any, Type, Tuple, Optional
from functools import wraps
import logging
from .exceptions import APIError, AuthenticationError

logger = logging.getLogger(__name__)


class RetryConfig:
    """Configuration for retry behavior."""
    
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: Tuple[Type[Exception], ...] = (APIError,),
        non_retryable_status_codes: Tuple[int, ...] = (400, 401, 403, 404, 422),
    ):
        """
        Initialize retry configuration.
        
        :param max_attempts: Maximum number of retry attempts
        :param base_delay: Base delay in seconds before first retry
        :param max_delay: Maximum delay between retries
        :param exponential_base: Base for exponential backoff
        :param jitter: Whether to add random jitter to delays
        :param retryable_exceptions: Exception types that should trigger retries
        :param non_retryable_status_codes: HTTP status codes that should not be retried
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions
        self.non_retryable_status_codes = non_retryable_status_codes


def should_retry(exception: Exception, config: RetryConfig) -> bool:
    """
    Determine if an exception should trigger a retry.
    
    :param exception: The exception that occurred
    :param config: Retry configuration
    :return: True if should retry, False otherwise
    """
    # Don't retry non-retryable exception types
    if not isinstance(exception, config.retryable_exceptions):
        return False
    
    # For API errors, check status codes
    if isinstance(exception, APIError):
        if exception.status_code in config.non_retryable_status_codes:
            return False
    
    # Never retry authentication errors
    if isinstance(exception, AuthenticationError):
        return False
    
    return True


def calculate_delay(attempt: int, config: RetryConfig) -> float:
    """
    Calculate delay before next retry attempt.
    
    :param attempt: Current attempt number (0-based)
    :param config: Retry configuration
    :return: Delay in seconds
    """
    if attempt == 0:
        return 0  # No delay for first attempt
    
    # Calculate exponential backoff
    delay = config.base_delay * (config.exponential_base ** (attempt - 1))
    
    # Cap at max delay
    delay = min(delay, config.max_delay)
    
    # Add jitter if enabled
    if config.jitter:
        jitter_range = delay * 0.1  # 10% jitter
        delay += random.uniform(-jitter_range, jitter_range)
    
    return max(0, delay)


def retry_on_failure(config: Optional[RetryConfig] = None):
    """
    Decorator to add retry logic to functions.
    
    :param config: Retry configuration. Uses defaults if None.
    :return: Decorated function
    """
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(config.max_attempts):
                try:
                    # Calculate and apply delay (except for first attempt)
                    delay = calculate_delay(attempt, config)
                    if delay > 0:
                        logger.debug(f"Retrying {func.__name__} in {delay:.2f}s (attempt {attempt + 1}/{config.max_attempts})")
                        time.sleep(delay)
                    
                    # Attempt the function call
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    
                    # Check if we should retry this exception
                    if not should_retry(e, config):
                        logger.debug(f"Not retrying {func.__name__}: non-retryable exception {type(e).__name__}")
                        raise
                    
                    # If this is the last attempt, don't log retry message
                    if attempt == config.max_attempts - 1:
                        logger.warning(f"Final attempt failed for {func.__name__}: {e}")
                        break
                    
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
            
            # All attempts failed, raise the last exception
            if last_exception:
                raise last_exception
            
            # This shouldn't happen, but just in case
            raise RuntimeError(f"All retry attempts failed for {func.__name__}")
        
        return wrapper
    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for reliability.
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: Type[Exception] = APIError
    ):
        """
        Initialize circuit breaker.
        
        :param failure_threshold: Number of failures before opening circuit
        :param recovery_timeout: Time to wait before attempting recovery
        :param expected_exception: Exception type that counts as failure
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        # State tracking
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def __call__(self, func: Callable) -> Callable:
        """Use as decorator."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call function with circuit breaker protection.
        
        :param func: Function to call
        :param args: Function arguments
        :param kwargs: Function keyword arguments
        :return: Function result
        :raises: CircuitBreakerOpenError if circuit is open
        """
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass


# Default retry configurations for different scenarios
DEFAULT_RETRY_CONFIG = RetryConfig()

AGGRESSIVE_RETRY_CONFIG = RetryConfig(
    max_attempts=5,
    base_delay=0.5,
    max_delay=30.0,
    exponential_base=1.5
)

CONSERVATIVE_RETRY_CONFIG = RetryConfig(
    max_attempts=2,
    base_delay=2.0,
    max_delay=10.0,
    exponential_base=2.0
)
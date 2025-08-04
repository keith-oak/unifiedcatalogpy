"""
Tests for retry logic and reliability features.
"""

import pytest
import time
from unittest.mock import Mock, patch

from unifiedcatalogpy.retry import (
    RetryConfig, should_retry, calculate_delay, retry_on_failure,
    CircuitBreaker, CircuitBreakerOpenError, DEFAULT_RETRY_CONFIG
)
from unifiedcatalogpy.exceptions import APIError, AuthenticationError, ValidationError


class TestRetryConfig:
    """Test RetryConfig class."""
    
    def test_default_config(self):
        """Test default retry configuration."""
        config = RetryConfig()
        
        assert config.max_attempts == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True
        assert APIError in config.retryable_exceptions
        assert 400 in config.non_retryable_status_codes
    
    def test_custom_config(self):
        """Test custom retry configuration."""
        config = RetryConfig(
            max_attempts=5,
            base_delay=0.5,
            max_delay=30.0,
            exponential_base=1.5,
            jitter=False
        )
        
        assert config.max_attempts == 5
        assert config.base_delay == 0.5
        assert config.max_delay == 30.0
        assert config.exponential_base == 1.5
        assert config.jitter is False


class TestShouldRetry:
    """Test should_retry function."""
    
    def test_retryable_exceptions(self):
        """Test retryable exceptions."""
        config = RetryConfig()
        
        # APIError with retryable status code (500)
        api_error = APIError("Server error", 500)
        assert should_retry(api_error, config) is True
        
        # APIError with non-retryable status code (400)
        client_error = APIError("Bad request", 400)
        assert should_retry(client_error, config) is False
        
        # APIError with non-retryable status code (404)
        not_found_error = APIError("Not found", 404)
        assert should_retry(not_found_error, config) is False
    
    def test_non_retryable_exceptions(self):
        """Test non-retryable exceptions."""
        config = RetryConfig()
        
        # AuthenticationError should never be retried
        auth_error = AuthenticationError("Invalid credentials")
        assert should_retry(auth_error, config) is False
        
        # ValidationError is not in retryable_exceptions
        validation_error = ValidationError("Invalid input")
        assert should_retry(validation_error, config) is False
        
        # Generic Exception is not in retryable_exceptions
        generic_error = Exception("Something went wrong")
        assert should_retry(generic_error, config) is False


class TestCalculateDelay:
    """Test calculate_delay function."""
    
    def test_no_delay_first_attempt(self):
        """Test no delay for first attempt."""
        config = RetryConfig()
        delay = calculate_delay(0, config)
        assert delay == 0
    
    def test_exponential_backoff(self):
        """Test exponential backoff calculation."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=False)
        
        # Second attempt (attempt=1): 1.0 * 2^0 = 1.0
        delay1 = calculate_delay(1, config)
        assert delay1 == 1.0
        
        # Third attempt (attempt=2): 1.0 * 2^1 = 2.0
        delay2 = calculate_delay(2, config)
        assert delay2 == 2.0
        
        # Fourth attempt (attempt=3): 1.0 * 2^2 = 4.0
        delay3 = calculate_delay(3, config)
        assert delay3 == 4.0
    
    def test_max_delay_cap(self):
        """Test maximum delay cap."""
        config = RetryConfig(base_delay=10.0, max_delay=15.0, exponential_base=2.0, jitter=False)
        
        # Attempt that would result in delay > max_delay
        delay = calculate_delay(5, config)  # Would be 10.0 * 2^4 = 160.0
        assert delay == 15.0  # Capped at max_delay
    
    def test_jitter(self):
        """Test jitter addition."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=True)
        
        delays = []
        for _ in range(10):
            delay = calculate_delay(1, config)
            delays.append(delay)
        
        # With jitter, delays should vary
        assert len(set(delays)) > 1  # Not all delays are the same
        
        # All delays should be positive and reasonably close to base value
        for delay in delays:
            assert delay > 0
            assert 0.8 <= delay <= 1.2  # Within jitter range


class TestRetryDecorator:
    """Test retry_on_failure decorator."""
    
    def test_successful_function(self):
        """Test function that succeeds on first attempt."""
        @retry_on_failure()
        def successful_function():
            return "success"
        
        result = successful_function()
        assert result == "success"
    
    def test_function_succeeds_after_retries(self):
        """Test function that succeeds after retries."""
        call_count = 0
        
        @retry_on_failure(RetryConfig(max_attempts=3, base_delay=0.01))
        def eventually_successful_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise APIError("Server error", 500)
            return "success"
        
        result = eventually_successful_function()
        assert result == "success"
        assert call_count == 3
    
    def test_function_fails_all_attempts(self):
        """Test function that fails all retry attempts."""
        call_count = 0
        
        @retry_on_failure(RetryConfig(max_attempts=2, base_delay=0.01))
        def always_failing_function():
            nonlocal call_count
            call_count += 1
            raise APIError("Server error", 500)
        
        with pytest.raises(APIError):
            always_failing_function()
        
        assert call_count == 2  # Called max_attempts times
    
    def test_non_retryable_exception(self):
        """Test function with non-retryable exception."""
        call_count = 0
        
        @retry_on_failure()
        def function_with_auth_error():
            nonlocal call_count
            call_count += 1
            raise AuthenticationError("Invalid credentials")
        
        with pytest.raises(AuthenticationError):
            function_with_auth_error()
        
        assert call_count == 1  # Not retried


class TestCircuitBreaker:
    """Test CircuitBreaker class."""
    
    def test_successful_calls(self):
        """Test circuit breaker with successful calls."""
        circuit_breaker = CircuitBreaker(failure_threshold=3)
        
        def successful_function():
            return "success"
        
        # Multiple successful calls should keep circuit closed
        for _ in range(10):
            result = circuit_breaker.call(successful_function)
            assert result == "success"
            assert circuit_breaker.state == "CLOSED"
    
    def test_circuit_opens_after_failures(self):
        """Test circuit breaker opens after threshold failures."""
        circuit_breaker = CircuitBreaker(failure_threshold=3)
        
        def failing_function():
            raise APIError("Server error", 500)
        
        # First few failures should not open circuit
        for i in range(2):
            with pytest.raises(APIError):
                circuit_breaker.call(failing_function)
            assert circuit_breaker.state == "CLOSED"
        
        # Third failure should open circuit
        with pytest.raises(APIError):
            circuit_breaker.call(failing_function)
        assert circuit_breaker.state == "OPEN"
        
        # Subsequent calls should raise CircuitBreakerOpenError
        with pytest.raises(CircuitBreakerOpenError):
            circuit_breaker.call(failing_function)
    
    def test_circuit_recovery(self):
        """Test circuit breaker recovery after timeout."""
        circuit_breaker = CircuitBreaker(
            failure_threshold=2, 
            recovery_timeout=0.1  # Very short timeout for testing
        )
        
        def failing_function():
            raise APIError("Server error", 500)
        
        def successful_function():
            return "success"
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(APIError):
                circuit_breaker.call(failing_function)
        assert circuit_breaker.state == "OPEN"
        
        # Wait for recovery timeout
        time.sleep(0.15)
        
        # Next call should attempt reset
        result = circuit_breaker.call(successful_function)
        assert result == "success"
        assert circuit_breaker.state == "CLOSED"
    
    def test_circuit_breaker_as_decorator(self):
        """Test circuit breaker used as decorator."""
        circuit_breaker = CircuitBreaker(failure_threshold=2)
        
        @circuit_breaker
        def decorated_function(should_fail=False):
            if should_fail:
                raise APIError("Server error", 500)
            return "success"
        
        # Successful calls
        assert decorated_function(False) == "success"
        
        # Open circuit with failures
        for _ in range(2):
            with pytest.raises(APIError):
                decorated_function(True)
        
        # Circuit should be open
        with pytest.raises(CircuitBreakerOpenError):
            decorated_function(False)


def test_default_configs():
    """Test default configuration constants."""
    assert DEFAULT_RETRY_CONFIG.max_attempts == 3
    assert DEFAULT_RETRY_CONFIG.base_delay == 1.0
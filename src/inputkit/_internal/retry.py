"""
retry.py

Internal retry logic for input and validation.

Provides RetryHandler class for managing retry attempts and backoff strategies.
Handles re-prompting users on invalid input and manages retry state.
Works with BaseInputHandler and validator functions.

Purpose:
- Provide a consistent retry mechanism for all input modules.
- Keep loops and error handling internal.
- Support configurable retry strategies.
"""

from typing import Optional, Callable, Any
from datetime import datetime, timedelta


class RetryHandler:
    """
    Handler for retry logic and attempt management.
    
    Manages retry attempts, tracks failures, and provides retry state information.
    """
    
    def __init__(
        self,
        max_attempts: int = 3,
        backoff_factor: float = 1.0,
        initial_delay: float = 0.0
    ):
        """
        Initialize retry handler.
        
        Args:
            max_attempts: Maximum number of retry attempts.
            backoff_factor: Multiplier for exponential backoff (1.0 = no backoff).
            initial_delay: Initial delay before first retry in seconds.
        """
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor
        self.initial_delay = initial_delay
        self.attempts = 0
        self.last_error: Optional[Exception] = None
        self.start_time: Optional[datetime] = None
    
    def reset(self) -> None:
        """Reset retry state."""
        self.attempts = 0
        self.last_error = None
        self.start_time = None
    
    def increment(self) -> None:
        """Increment attempt counter."""
        self.attempts += 1
        if self.start_time is None:
            self.start_time = datetime.now()
    
    def can_retry(self) -> bool:
        """
        Check if more retries are allowed.
        
        Returns:
            True if more retries are allowed, False otherwise.
        """
        return self.attempts < self.max_attempts
    
    def get_remaining_attempts(self) -> int:
        """
        Get remaining retry attempts.
        
        Returns:
            Number of remaining attempts.
        """
        return max(0, self.max_attempts - self.attempts)
    
    def get_delay(self) -> float:
        """
        Get delay before next retry (exponential backoff).
        
        Returns:
            Delay in seconds.
        """
        if self.attempts == 0:
            return 0.0
        return self.initial_delay * (self.backoff_factor ** (self.attempts - 1))
    
    def record_error(self, error: Exception) -> None:
        """
        Record an error for tracking.
        
        Args:
            error: The error that occurred.
        """
        self.last_error = error

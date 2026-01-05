"""
input.py

This module defines custom exceptions for user input errors in inputkit.

Classes:
    - InputError: Base exception for input-related problems.
    - InputCancelled: Raised when the user cancels input (Ctrl-C/Ctrl-D).
    - EmptyInputError: For empty submissions when input is required.
    - RetryLimitExceeded: Raised when retry count exceeds the maximum allowed.
    - InputInterrupted: Raised when input is interrupted by a signal or EOF.

These errors help clearly distinguish user, workflow, and system input issues.
"""
from .base import InputKitError

class InputError(InputKitError):
    """
    Base exception for all user input errors in inputkit.
    Args:
        message: Description of the input error.
        **context: Optional debug context.
    """
    def __init__(self, message=None, **context):
        if message is None:
            message = "A user input error occurred."
        self.context = context
        super().__init__(message)

class InputCancelled(InputError):
    """
    Raised if user cancels input (e.g., via Ctrl-C/Ctrl-D).
    """
    def __init__(self, message=None):
        if message is None:
            message = "Input cancelled by user."
        super().__init__(message)

class EmptyInputError(InputError):
    """
    Raised when user submits empty input.
    """
    def __init__(self, message=None):
        if message is None:
            message = "No input provided (empty value)."
        super().__init__(message)

class RetryLimitExceeded(InputError):
    """
    Raised when retry limit for obtaining input is exceeded.
    Args:
        attempts: Maximum allowed attempts.
    """
    def __init__(self, attempts=None, message=None):
        if message is None:
            message = f"Retry limit exceeded{f' after {attempts} attempts' if attempts is not None else ''}."
        super().__init__(message, attempts=attempts)

class InputInterrupted(InputError):
    """
    Raised when input is interrupted (Ctrl+C, Ctrl+D, signal, etc.).
    """
    def __init__(self, message=None):
        if message is None:
            message = "Input interrupted."
        super().__init__(message)

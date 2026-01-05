"""
exceptions

The inputkit.exceptions package contains all error and exception classes used in inputkit.

You can import any exception directly from this package to simplify error handling and maintain clean application code.

Available exceptions:
    - InputKitError (base)
    - ValidationError, RequiredValueError, InvalidTypeError, PatternMismatchError, LengthError,
      RangeError, PasswordStrengthError, ValidatorConfigurationError, MultiValidationError,
      InternalInputKitError
    - InputError, InputCancelled, EmptyInputError, RetryLimitExceeded, InputInterrupted
    - SystemError, UnsupportedPlatformError, TerminalNotAvailableError
"""
from .base import InputKitError
from .validation import (
    ValidationError, RequiredValueError, InvalidTypeError, PatternMismatchError, LengthError,
    RangeError, PasswordStrengthError, ValidatorConfigurationError, MultiValidationError,
    InternalInputKitError)
from .input import (
    InputError, InputCancelled, EmptyInputError, RetryLimitExceeded, InputInterrupted)
from .system import (
    SystemError, UnsupportedPlatformError, TerminalNotAvailableError)

__all__ = [
    "InputKitError",
    "ValidationError", "RequiredValueError", "InvalidTypeError", "PatternMismatchError", "LengthError",
    "RangeError", "PasswordStrengthError", "ValidatorConfigurationError", "MultiValidationError",
    "InternalInputKitError",
    "InputError", "InputCancelled", "EmptyInputError", "RetryLimitExceeded", "InputInterrupted",
    "SystemError", "UnsupportedPlatformError", "TerminalNotAvailableError"
]

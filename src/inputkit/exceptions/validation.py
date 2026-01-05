"""
validation.py

This module defines exception classes for input validation errors in inputkit.

Classes:
    - ValidationError: Base class for validation-related errors.
    - RequiredValueError: Indicates a required value is missing.
    - InvalidTypeError: Raised when a value has the wrong type.
    - PatternMismatchError: Raised when input does not match a pattern.
    - LengthError: Raised when input length is out of allowed range.
    - RangeError: Raised when numeric input is out of range.
    - PasswordStrengthError: Raised for passwords not meeting security needs.
    - ValidatorConfigurationError: Indicates a validator is misconfigured.
    - MultiValidationError: Represents multiple validation failures.
    - InternalInputKitError: For unexpected framework bugs.

These errors standardize reporting of all validation failures, making inputkit safer and easier to debug.
"""
from .base import InputKitError


class ValidationError(InputKitError):
    """
    Base exception for all validation errors in inputkit.

    Args:
        message: A description of the validation failure.
        field: (Optional) The input field or parameter involved.
        value: (Optional) The invalid value, if applicable.
        **context: Additional context for debugging.
    """
    def __init__(self, message=None, field=None, value=None, **context):
        if message is None:
            message = "Validation failed."
        self.field = field
        self.value = value
        self.context = context
        super().__init__(message)


class ValidatorConfigurationError(ValidationError):
    """
    Raised when a validator is misconfigured or called with improper arguments.

    Args:
        validator: Name of the validator.
        detail: Description of the configuration error.
    """
    def __init__(self, validator=None, detail=None, message=None):
        if message is None:
            message = f"Validator{f' {validator}' if validator else ''} is misconfigured: {detail or 'see documentation.'}"
        super().__init__(message, validator=validator, detail=detail)


class MultiValidationError(ValidationError):
    """
    Raised when multiple validation errors are encountered (e.g., in a form).

    Args:
        errors: List of ValidationError instances.
    """
    def __init__(self, errors, message=None):
        self.errors = errors
        if message is None:
            submessages = [str(e) for e in errors]
            message = f"Multiple validation errors occurred: {submessages}"
        super().__init__(message, errors=errors)


class RequiredValueError(ValidationError):
    """
    Raised when a required value is missing.

    Args:
        field: Optional name of the required field.
    """
    def __init__(self, field=None, message=None):
        if message is None:
            message = f"Required value{f' for {field}' if field else ''} is missing."
        super().__init__(message, field=field)


class InvalidTypeError(ValidationError):
    """
    Raised when the value type is incorrect.

    Args:
        expected: The expected type(s).
        actual: The received type.
        field: Optional field name.
    """
    def __init__(self, expected, actual, field=None, message=None):
        if message is None:
            message = f"Expected type {expected}, got {actual}{f' for {field}' if field else ''}."
        super().__init__(message, field=field, value=None, expected=expected, actual=actual)


class PatternMismatchError(ValidationError):
    """
    Raised when a value does not match the expected pattern (e.g. regex).

    Args:
        pattern: The regex/pattern expected.
        value: The value that failed.
        field: Optional name of the field.
    """
    def __init__(self, pattern, value, field=None, message=None):
        if message is None:
            message = f"Value does not match the expected pattern: {pattern}{f' for {field}' if field else ''}."
        super().__init__(message, pattern=pattern, value=value, field=field)


class LengthError(ValidationError):
    """
    Raised when string length constraints are violated.

    Args:
        min_length: Minimum allowed length.
        max_length: Maximum allowed length.
        actual_length: The offending value's length.
        field: Optional name of the field.
    """
    def __init__(self, min_length=None, max_length=None, actual_length=None, field=None, message=None):
        if message is None:
            message = (
                f"Value length {actual_length} not in allowed range"
                f"{f' [{min_length}, {max_length}]' if min_length is not None or max_length is not None else ''}"
                f"{f' for {field}' if field else ''}."
            )
        super().__init__(message, field=field, min_length=min_length, max_length=max_length, actual_length=actual_length)


class RangeError(ValidationError):
    """
    Raised when numeric values are out of allowed range.

    Args:
        min_value: Minimal allowed.
        max_value: Maximum allowed.
        actual_value: The offending value.
        field: Optional field name.
    """
    def __init__(self, min_value=None, max_value=None, actual_value=None, field=None, message=None):
        if message is None:
            message = (
                f"Value {actual_value} out of range"
                f"{f' [{min_value},{max_value}]' if min_value is not None or max_value is not None else ''}"
                f"{f' for {field}' if field else ''}."
            )
        super().__init__(message, field=field, min_value=min_value, max_value=max_value, actual_value=actual_value)


class PasswordStrengthError(ValidationError):
    """
    Raised when a password does not meet security requirements.

    Args:
        reasons: (Optional) List of password deficiencies.
        field: Optional field name.
    """
    def __init__(self, reasons=None, field=None, message=None):
        if message is None:
            base = "Password does not meet the required strength criteria."
            if reasons:
                base += f" Deficiencies: {', '.join(reasons)}."
            if field:
                base += f" (Field: {field})"
            message = base
        super().__init__(message, reasons=reasons, field=field)


class InternalInputKitError(ValidationError):
    """
    Raised for unexpected internal bugs or logical failures in the validation framework itself.
    Args:
        detail: What failed internally.
    """
    def __init__(self, detail=None, message=None):
        if message is None:
            message = f"Internal inputkit validation error: {detail or 'Unknown bug.'}"
        super().__init__(message, detail=detail)

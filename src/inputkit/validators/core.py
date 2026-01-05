"""
core.py

Private core logic for all validators.

This module provides the base validator class and shared internal functions for all validation logic.
Handles common behaviors such as chaining, combining, and error reporting.

Purpose:
- Encapsulate the internal implementation.
- Keep public API clean and stable.
- Provide reusable base functionality for all validators.
"""

import re
from typing import Optional, Pattern, Callable, Any, List
from abc import ABC, abstractmethod

from ..exceptions import ValidationError, PatternMismatchError


class BaseValidator(ABC):
    """
    Abstract base class for all validators in inputkit.
    
    Provides common functionality for validation, custom regex support, and error handling.
    All validators should inherit from this class to ensure consistent behavior.
    
    Attributes:
        custom_pattern: Optional custom regex pattern provided by the user.
        field_name: Optional field name for better error messages.
    """
    
    def __init__(self, custom_pattern: Optional[Pattern] = None, field_name: Optional[str] = None):
        """
        Initialize the base validator.
        
        Args:
            custom_pattern: Optional custom regex pattern to use instead of default.
            field_name: Optional name of the field being validated (for error messages).
        """
        self.custom_pattern = custom_pattern
        self.field_name = field_name
    
    @abstractmethod
    def validate(self, value: Any) -> bool:
        """
        Validate a value.
        
        Args:
            value: The value to validate.
            
        Returns:
            True if validation passes, False otherwise.
            
        Raises:
            ValidationError: If validation fails and should raise an exception.
        """
        pass
    
    def _raise_validation_error(self, message: str, value: Any = None, **context) -> None:
        """
        Raise a validation error with proper context.
        
        Args:
            message: Error message.
            value: The invalid value.
            **context: Additional context for the error.
        """
        raise ValidationError(message=message, field=self.field_name, value=value, **context)
    
    def _match_pattern(self, value: str, pattern: Pattern, error_message: Optional[str] = None) -> bool:
        """
        Match a value against a regex pattern.
        
        Args:
            value: The string value to match.
            pattern: The regex pattern to match against.
            error_message: Optional custom error message.
            
        Returns:
            True if pattern matches.
            
        Raises:
            PatternMismatchError: If pattern doesn't match.
        """
        if not isinstance(value, str):
            self._raise_validation_error(
                f"Expected string, got {type(value).__name__}",
                value=value
            )
        
        if pattern.fullmatch(value):
            return True
        
        msg = error_message or f"Value does not match required pattern for {self.field_name or 'field'}"
        raise PatternMismatchError(
            pattern=str(pattern.pattern),
            value=value,
            field=self.field_name,
            message=msg
        )


class CompositeValidator(BaseValidator):
    """
    Validator that combines multiple validators.
    
    Useful for complex validation scenarios where multiple checks are needed.
    """
    
    def __init__(self, validators: List[BaseValidator], field_name: Optional[str] = None):
        """
        Initialize composite validator.
        
        Args:
            validators: List of validators to apply.
            field_name: Optional field name.
        """
        super().__init__(field_name=field_name)
        self.validators = validators
    
    def validate(self, value: Any) -> bool:
        """
        Validate value against all validators.
        
        Args:
            value: The value to validate.
            
        Returns:
            True if all validators pass.
            
        Raises:
            ValidationError: If any validator fails.
        """
        errors = []
        for validator in self.validators:
            try:
                validator.validate(value)
            except ValidationError as e:
                errors.append(e)
        
        if errors:
            from ..exceptions import MultiValidationError
            raise MultiValidationError(errors)
        
        return True

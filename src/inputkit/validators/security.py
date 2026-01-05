"""
security.py

Validation rules for sensitive input such as passwords, PINs, API keys, and tokens in inputkit.

This module provides:
- Password strength validation
- PIN validation (4-12 digits)
- API key format validation
- Token validation (JWT, hex, base64)
- Secret text validation

All validators support custom patterns and provide security-focused error messages.

Purpose:
- Provide ready-to-use security validators.
- Help developers enforce best practices for sensitive data input.
- Enable flexible validation with custom security requirements.
"""

import re
from typing import Optional, Pattern, Any, List

from .core import BaseValidator
from .patterns import PinPattern, ApiKeyPattern, TokenPattern
from ..exceptions import PasswordStrengthError, ValidationError, LengthError


class PasswordValidator(BaseValidator):
    """
    Validator for password strength and security requirements.
    
    Enforces password strength rules including minimum length, character requirements,
    and complexity checks. Supports custom patterns for specialized password policies.
    """
    
    def __init__(
        self,
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize password validator.
        
        Args:
            min_length: Minimum password length (default: 8).
            require_uppercase: Require at least one uppercase letter.
            require_lowercase: Require at least one lowercase letter.
            require_digit: Require at least one digit.
            require_special: Require at least one special character.
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
    
    def validate(self, value: Any) -> bool:
        """
        Validate password strength.
        
        Args:
            value: The password string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            PasswordStrengthError: If password doesn't meet requirements.
        """
        if not isinstance(value, str):
            self._raise_validation_error(
                f"Expected string, got {type(value).__name__}",
                value=value
            )
        
        if self.custom_pattern:
            self._match_pattern(value, self.custom_pattern)
        
        reasons = []
        
        # Length check
        if len(value) < self.min_length:
            reasons.append(f"Password must be at least {self.min_length} characters long")
        
        # Character requirement checks
        if self.require_uppercase and not re.search(r'[A-Z]', value):
            reasons.append("Password must contain at least one uppercase letter")
        
        if self.require_lowercase and not re.search(r'[a-z]', value):
            reasons.append("Password must contain at least one lowercase letter")
        
        if self.require_digit and not re.search(r'\d', value):
            reasons.append("Password must contain at least one digit")
        
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            reasons.append("Password must contain at least one special character")
        
        if reasons:
            raise PasswordStrengthError(
                reasons=reasons,
                field=self.field_name,
                message=f"Password does not meet security requirements: {', '.join(reasons)}"
            )
        
        return True


class PinValidator(BaseValidator):
    """
    Validator for PIN codes (typically 4-12 digits).
    
    Validates numeric PIN formats. Supports custom patterns for specialized PIN formats.
    """
    
    def __init__(
        self,
        min_length: int = 4,
        max_length: int = 12,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize PIN validator.
        
        Args:
            min_length: Minimum PIN length (default: 4).
            max_length: Maximum PIN length (default: 12).
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = re.compile(rf"^\d{{{min_length},{max_length}}}$")
    
    def validate(self, value: Any) -> bool:
        """
        Validate PIN code.
        
        Args:
            value: The PIN string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, str):
            value = str(value)
        
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"PIN must be {self.min_length}-{self.max_length} digits for {self.field_name or 'field'}"
        )
        return True


class ApiKeyValidator(BaseValidator):
    """
    Validator for API keys (typically 32-128 alphanumeric characters).
    
    Validates API key formats. Supports custom patterns for specialized API key formats.
    """
    
    def __init__(
        self,
        min_length: int = 32,
        max_length: int = 128,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize API key validator.
        
        Args:
            min_length: Minimum API key length (default: 32).
            max_length: Maximum API key length (default: 128).
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = ApiKeyPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate API key.
        
        Args:
            value: The API key string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, str):
            self._raise_validation_error(
                f"Expected string, got {type(value).__name__}",
                value=value
            )
        
        length = len(value)
        if length < self.min_length or length > self.max_length:
            raise LengthError(
                min_length=self.min_length,
                max_length=self.max_length,
                actual_length=length,
                field=self.field_name,
                message=f"API key must be {self.min_length}-{self.max_length} characters long"
            )
        
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid API key format for {self.field_name or 'field'}"
        )
        return True


class TokenValidator(BaseValidator):
    """
    Validator for tokens (JWT, hex, base64, etc.).
    
    Validates token formats. Supports custom patterns for specialized token formats.
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize token validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.pattern = TokenPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate token.
        
        Args:
            value: The token string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, str):
            self._raise_validation_error(
                f"Expected string, got {type(value).__name__}",
                value=value
            )
        
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid token format for {self.field_name or 'field'}"
        )
        return True


class SecretTextValidator(BaseValidator):
    """
    Validator for secret/hidden text input.
    
    Similar to plain text but with additional security considerations.
    Validates that secret text meets minimum security requirements.
    """
    
    def __init__(
        self,
        min_length: int = 1,
        max_length: Optional[int] = None,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize secret text validator.
        
        Args:
            min_length: Minimum secret text length (default: 1).
            max_length: Maximum secret text length (None for no limit).
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any) -> bool:
        """
        Validate secret text.
        
        Args:
            value: The secret text string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, str):
            self._raise_validation_error(
                f"Expected string, got {type(value).__name__}",
                value=value
            )
        
        length = len(value)
        if length < self.min_length:
            raise LengthError(
                min_length=self.min_length,
                actual_length=length,
                field=self.field_name,
                message=f"Secret text must be at least {self.min_length} characters long"
            )
        
        if self.max_length and length > self.max_length:
            raise LengthError(
                max_length=self.max_length,
                actual_length=length,
                field=self.field_name,
                message=f"Secret text must be at most {self.max_length} characters long"
            )
        
        if self.custom_pattern:
            self._match_pattern(value, self.custom_pattern)
        
        return True

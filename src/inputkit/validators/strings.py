"""
strings.py

Validation rules for string-based input in inputkit.

This module provides object-oriented validators for all textual input types including:
- Plain text (with length constraints)
- Username and slug/identifier validation
- Full name validation (multilingual support)
- Email, URL, file path validation
- Command string validation
- Multiline text detection

All validators support custom regex patterns and provide user-friendly error messages.

Purpose:
- Provide reusable string validation logic.
- Keep string-related validators separate from numeric or pattern validators.
- Enable flexible validation with custom patterns.
"""

import re
from typing import Optional, Pattern, Any

from .core import BaseValidator
from .patterns import (
    UsernamePattern, FullNamePattern, EmailPattern, URLPattern,
    FilePathPattern, CommandPattern, MultiLineTextPattern
)
from ..exceptions import LengthError, ValidationError


class PlainTextValidator(BaseValidator):
    """
    Validator for plain text input with optional length constraints.
    
    Validates that input is a non-empty string and optionally checks length bounds.
    Supports custom regex patterns for additional constraints.
    """
    
    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize plain text validator.
        
        Args:
            min_length: Minimum allowed length (inclusive).
            max_length: Maximum allowed length (inclusive).
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any) -> bool:
        """
        Validate plain text input.
        
        Args:
            value: The text value to validate.
            
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
        
        if not value.strip():
            self._raise_validation_error(
                f"Text cannot be empty for {self.field_name or 'field'}",
                value=value
            )
        
        length = len(value)
        if self.min_length is not None and length < self.min_length:
            raise LengthError(
                min_length=self.min_length,
                actual_length=length,
                field=self.field_name,
                message=f"Text must be at least {self.min_length} characters long"
            )
        
        if self.max_length is not None and length > self.max_length:
            raise LengthError(
                max_length=self.max_length,
                actual_length=length,
                field=self.field_name,
                message=f"Text must be at most {self.max_length} characters long"
            )
        
        if self.custom_pattern:
            self._match_pattern(value, self.custom_pattern)
        
        return True


class UsernameValidator(BaseValidator):
    """
    Validator for usernames and identifiers.
    
    Supports both strict (ASCII only) and relaxed (Unicode) modes.
    Can accept custom regex patterns for specialized username rules.
    """
    
    def __init__(
        self,
        strict: bool = True,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize username validator.
        
        Args:
            strict: If True, use strict ASCII-only pattern. If False, allow Unicode.
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.strict = strict
        self.pattern = UsernamePattern.STRICT if strict else UsernamePattern.RELAXED
    
    def validate(self, value: Any) -> bool:
        """
        Validate username.
        
        Args:
            value: The username string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid username format for {self.field_name or 'field'}"
        )
        return True


class FullNameValidator(BaseValidator):
    """
    Validator for full names with multilingual support.
    
    Allows letters, spaces, hyphens, and apostrophes. Supports Unicode characters
    for international names. Can accept custom patterns for specialized name formats.
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize full name validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.pattern = FullNamePattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate full name.
        
        Args:
            value: The full name string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid full name format for {self.field_name or 'field'}"
        )
        return True


class EmailValidator(BaseValidator):
    """
    Validator for email addresses using RFC 5322-compliant patterns.
    
    Supports standard email validation and custom regex patterns for specialized domains.
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize email validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.pattern = EmailPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate email address.
        
        Args:
            value: The email string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid email format for {self.field_name or 'field'}"
        )
        return True


class URLValidator(BaseValidator):
    """
    Validator for URLs (HTTP, HTTPS, FTP, file protocols).
    
    Supports standard URL validation and custom regex patterns.
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize URL validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.pattern = URLPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate URL.
        
        Args:
            value: The URL string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid URL format for {self.field_name or 'field'}"
        )
        return True


class FilePathValidator(BaseValidator):
    """
    Validator for file paths (Unix and Windows).
    
    Supports both absolute and relative paths. Can accept custom patterns.
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize file path validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.pattern = FilePathPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate file path.
        
        Args:
            value: The file path string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid file path format for {self.field_name or 'field'}"
        )
        return True


class CommandValidator(BaseValidator):
    """
    Validator for CLI command strings.
    
    Validates that command strings don't contain dangerous shell metacharacters.
    Supports custom patterns for specialized command formats.
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize command validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.pattern = CommandPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate command string.
        
        Args:
            value: The command string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid command format for {self.field_name or 'field'}"
        )
        return True


class MultiLineTextValidator(BaseValidator):
    """
    Validator for multiline text input.
    
    Detects and validates text that spans multiple lines. Useful for textarea inputs.
    """
    
    def __init__(
        self,
        min_lines: Optional[int] = None,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize multiline text validator.
        
        Args:
            min_lines: Minimum number of lines required (default: 2).
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.min_lines = min_lines or 2
        self.pattern = MultiLineTextPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate multiline text.
        
        Args:
            value: The multiline text string to validate.
            
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
        
        lines = value.split('\n')
        if len(lines) < self.min_lines:
            self._raise_validation_error(
                f"Text must contain at least {self.min_lines} lines",
                value=value
            )
        
        if self.custom_pattern:
            self._match_pattern(value, self.custom_pattern)
        elif not self.pattern.match(value):
            self._raise_validation_error(
                f"Invalid multiline text format for {self.field_name or 'field'}",
                value=value
            )
        
        return True


class SlugValidator(BaseValidator):
    """
    Validator for URL-friendly slugs and identifiers.
    
    Similar to username validator but typically more restrictive (lowercase, hyphens only).
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize slug validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        # Slug pattern: lowercase letters, numbers, hyphens only
        self.pattern = re.compile(r"^[a-z0-9-]{3,64}$")
    
    def validate(self, value: Any) -> bool:
        """
        Validate slug.
        
        Args:
            value: The slug string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid slug format for {self.field_name or 'field'}"
        )
        return True

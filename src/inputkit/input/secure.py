"""
secure.py

This module handles sensitive or hidden input from the user, like passwords.

Provides input handlers for:
- Password input (with strength validation)
- PIN input
- API key input
- Token input
- Secret text input (hidden)

All handlers hide input characters in the terminal and support validators.

Purpose:
- Provide secure and user-friendly input for secrets.
- Ensures privacy while keeping developer API simple.
"""

from typing import Optional, Pattern

from .core import BaseInputHandler
from ..validators.core import BaseValidator
from ..validators.security import (
    PasswordValidator, PinValidator, ApiKeyValidator,
    TokenValidator, SecretTextValidator
)


class PasswordInputHandler(BaseInputHandler):
    """
    Handler for password input with strength validation.
    
    Hides input characters and validates password strength.
    """
    
    def __init__(
        self,
        prompt: str = "Enter password",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize password input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value (not recommended for passwords).
            validator: Optional custom validator.
            min_length: Minimum password length.
            require_uppercase: Require uppercase letter.
            require_lowercase: Require lowercase letter.
            require_digit: Require digit.
            require_special: Require special character.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = PasswordValidator(
                min_length=min_length,
                require_uppercase=require_uppercase,
                require_lowercase=require_lowercase,
                require_digit=require_digit,
                require_special=require_special,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read password input (hidden)."""
        return self.terminal.read_secure(self._format_prompt())
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to password string."""
        return raw_input


class PinInputHandler(BaseInputHandler):
    """
    Handler for PIN code input (hidden).
    """
    
    def __init__(
        self,
        prompt: str = "Enter PIN",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        min_length: int = 4,
        max_length: int = 12,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize PIN input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value (not recommended for PINs).
            validator: Optional custom validator.
            min_length: Minimum PIN length.
            max_length: Maximum PIN length.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = PinValidator(
                min_length=min_length,
                max_length=max_length,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read PIN input (hidden)."""
        return self.terminal.read_secure(self._format_prompt())
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to PIN string."""
        return raw_input


class ApiKeyInputHandler(BaseInputHandler):
    """
    Handler for API key input (hidden).
    """
    
    def __init__(
        self,
        prompt: str = "Enter API key",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        min_length: int = 32,
        max_length: int = 128,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize API key input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            min_length: Minimum API key length.
            max_length: Maximum API key length.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = ApiKeyValidator(
                min_length=min_length,
                max_length=max_length,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read API key input (hidden)."""
        return self.terminal.read_secure(self._format_prompt())
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to API key string."""
        return raw_input


class TokenInputHandler(BaseInputHandler):
    """
    Handler for token input (hidden).
    """
    
    def __init__(
        self,
        prompt: str = "Enter token",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize token input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = TokenValidator(
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read token input (hidden)."""
        return self.terminal.read_secure(self._format_prompt())
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to token string."""
        return raw_input


class SecretTextInputHandler(BaseInputHandler):
    """
    Handler for secret text input (hidden).
    """
    
    def __init__(
        self,
        prompt: str = "Enter secret text",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        min_length: int = 1,
        max_length: Optional[int] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize secret text input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            min_length: Minimum secret text length.
            max_length: Maximum secret text length.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = SecretTextValidator(
                min_length=min_length,
                max_length=max_length,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read secret text input (hidden)."""
        return self.terminal.read_secure(self._format_prompt())
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to secret text string."""
        return raw_input

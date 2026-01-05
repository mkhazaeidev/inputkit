"""
text.py

This module provides classes for getting textual input from the user.

Provides input handlers for:
- Plain text input
- Username input
- Full name input
- Email input
- URL input
- File path input
- Command input
- Multiline text input
- Slug/identifier input

All handlers support validators, retry logic, defaults, and help text.

Purpose:
- Allow developers to ask for string inputs naturally.
- Can be extended for custom text-based input scenarios.
- Provide user-friendly input collection with validation.
"""

from typing import Optional, Pattern
import re

from .core import BaseInputHandler
from ..validators.core import BaseValidator
from ..exceptions import InputCancelled
from ..validators.strings import (
    PlainTextValidator, UsernameValidator, FullNameValidator, EmailValidator,
    URLValidator, FilePathValidator, CommandValidator, MultiLineTextValidator,
    SlugValidator
)


class PlainTextInputHandler(BaseInputHandler):
    """
    Handler for plain text input with optional length constraints.
    
    Supports custom validators and length constraints.
    """
    
    def __init__(
        self,
        prompt: str = "Enter text",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize plain text input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            min_length: Minimum text length.
            max_length: Maximum text length.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = PlainTextValidator(
                min_length=min_length,
                max_length=max_length,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read plain text input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to string."""
        return raw_input.strip()


class UsernameInputHandler(BaseInputHandler):
    """
    Handler for username input.
    
    Supports strict (ASCII) or relaxed (Unicode) modes.
    """
    
    def __init__(
        self,
        prompt: str = "Enter username",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        strict: bool = True,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize username input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            strict: If True, use strict ASCII-only validation.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = UsernameValidator(
                strict=strict,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read username input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to username string."""
        return raw_input.strip()


class FullNameInputHandler(BaseInputHandler):
    """
    Handler for full name input with multilingual support.
    """
    
    def __init__(
        self,
        prompt: str = "Enter full name",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize full name input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = FullNameValidator(
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read full name input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to full name string."""
        return raw_input.strip()


class EmailInputHandler(BaseInputHandler):
    """
    Handler for email address input.
    """
    
    def __init__(
        self,
        prompt: str = "Enter email",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize email input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = EmailValidator(
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read email input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to email string."""
        return raw_input.strip().lower()


class URLInputHandler(BaseInputHandler):
    """
    Handler for URL input.
    """
    
    def __init__(
        self,
        prompt: str = "Enter URL",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize URL input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = URLValidator(
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read URL input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to URL string."""
        return raw_input.strip()


class FilePathInputHandler(BaseInputHandler):
    """
    Handler for file path input (Unix and Windows).
    """
    
    def __init__(
        self,
        prompt: str = "Enter file path",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize file path input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = FilePathValidator(
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read file path input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to file path string."""
        return raw_input.strip()


class CommandInputHandler(BaseInputHandler):
    """
    Handler for CLI command input.
    """
    
    def __init__(
        self,
        prompt: str = "Enter command",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize command input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = CommandValidator(
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read command input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to command string."""
        return raw_input.strip()


class MultiLineTextInputHandler(BaseInputHandler):
    """
    Handler for multiline text input.
    
    Reads multiple lines until user enters a termination sequence (default: empty line).
    """
    
    def __init__(
        self,
        prompt: str = "Enter multiline text (end with empty line)",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        termination_line: str = "",
        min_lines: Optional[int] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize multiline text input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            termination_line: Line that signals end of input (default: empty line).
            min_lines: Minimum number of lines required.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = MultiLineTextValidator(
                min_lines=min_lines,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.termination_line = termination_line
    
    def _read_input(self) -> str:
        """Read multiline text input."""
        lines = []
        self.terminal.write(self.prompt + "\n")
        self.terminal.write("(Enter empty line to finish)\n")
        
        while True:
            try:
                line = self.terminal.read_line()
                if line == self.termination_line:
                    break
                lines.append(line)
            except (KeyboardInterrupt, EOFError):
                raise InputCancelled()
        
        return "\n".join(lines)
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to multiline text string."""
        return raw_input


class SlugInputHandler(BaseInputHandler):
    """
    Handler for slug/identifier input.
    """
    
    def __init__(
        self,
        prompt: str = "Enter slug",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize slug input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = SlugValidator(
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read slug input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to slug string."""
        return raw_input.strip().lower()

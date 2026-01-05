"""
core.py

This module contains the base classes and core logic for all input operations.

Provides BaseInputHandler as the parent class for all input types.
Handles retry logic, default values, error management, timeout, and cancellation.
Used internally by other input modules (text, secure, numeric, choices).

Purpose:
- Serve as the foundation for all user input functions.
- Keep common behaviors (like validation loops, prompts, retry) in one place.
- Provide consistent API across all input types.
"""

import sys
import signal
from typing import Optional, Callable, Any, Union
from abc import ABC, abstractmethod

from ..exceptions import InputError, InputCancelled, InputInterrupted, RetryLimitExceeded, EmptyInputError, ValidationError
from ..validators.core import BaseValidator
from .._internal.retry import RetryHandler
from ..system.terminal import TerminalManager


class BaseInputHandler(ABC):
    """
    Abstract base class for all input handlers in inputkit.
    
    Provides common functionality for:
    - Prompt display and formatting
    - Input validation with retry logic
    - Default values and optional inputs
    - Timeout handling
    - Cancellation/interruption handling (Ctrl+C, Ctrl+D)
    - Help/hint display
    - Error handling and user-friendly messages
    
    All input handlers should inherit from this class.
    """
    
    def __init__(
        self,
        prompt: str = "",
        default: Optional[Any] = None,
        validator: Optional[BaseValidator] = None,
        required: bool = True,
        retry_limit: int = 3,
        retry_message: Optional[str] = None,
        help_text: Optional[str] = None,
        hint: Optional[str] = None,
        timeout: Optional[float] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize base input handler.
        
        Args:
            prompt: The prompt text to display to the user.
            default: Default value if input is empty and not required.
            validator: Optional validator instance to validate input.
            required: If False, allows empty input (returns default or None).
            retry_limit: Maximum number of retry attempts on validation failure.
            retry_message: Custom message to display on retry (default: auto-generated).
            help_text: Help text to display when user requests help (e.g., '?').
            hint: Hint text to display below the prompt.
            timeout: Timeout in seconds (None for no timeout).
            field_name: Name of the field (for error messages).
        """
        self.prompt = prompt
        self.default = default
        self.validator = validator
        self.required = required
        self.retry_limit = retry_limit
        self.retry_message = retry_message
        self.help_text = help_text
        self.hint = hint
        self.timeout = timeout
        self.field_name = field_name or "input"
        
        self.terminal = TerminalManager()
        self.retry_handler = RetryHandler(max_attempts=retry_limit)
    
    @abstractmethod
    def _read_input(self) -> str:
        """
        Read raw input from the user.
        
        Must be implemented by subclasses to handle different input types
        (e.g., secure input for passwords, multiline for text areas).
        
        Returns:
            Raw input string from user.
            
        Raises:
            InputInterrupted: If input is interrupted (Ctrl+C, Ctrl+D).
        """
        pass
    
    def _format_prompt(self) -> str:
        """
        Format the prompt with default value and hint indicators.
        
        Returns:
            Formatted prompt string.
        """
        prompt_parts = [self.prompt]
        
        if self.default is not None:
            prompt_parts.append(f"[default: {self.default}]")
        
        if not self.required:
            prompt_parts.append("(optional)")
        
        if self.help_text:
            prompt_parts.append("(type '?' for help)")
        
        prompt_str = " ".join(prompt_parts) + ": "
        
        if self.hint:
            prompt_str += f"\n  Hint: {self.hint}\n"
        
        return prompt_str
    
    def _handle_help_request(self, user_input: str) -> bool:
        """
        Check if user requested help and display it.
        
        Args:
            user_input: The user's input string.
            
        Returns:
            True if help was requested and displayed, False otherwise.
        """
        if user_input.strip() == "?" and self.help_text:
            self.terminal.write(self.help_text + "\n")
            return True
        return False
    
    def _process_input(self, raw_input: str) -> Any:
        """
        Process raw input: handle empty, default, and validation.
        
        Args:
            raw_input: Raw input string from user.
            
        Returns:
            Processed input value.
            
        Raises:
            ValidationError: If validation fails.
            EmptyInputError: If input is empty and required.
        """
        # Handle help request
        if self._handle_help_request(raw_input):
            return None  # Signal to retry
        
        # Handle empty input
        if not raw_input.strip():
            if not self.required:
                return self.default
            if self.default is not None:
                return self.default
            raise EmptyInputError()
        
        # Validate if validator provided
        if self.validator:
            self.validator.validate(raw_input)
        
        return self._convert_value(raw_input)
    
    @abstractmethod
    def _convert_value(self, raw_input: str) -> Any:
        """
        Convert raw input string to appropriate type.
        
        Must be implemented by subclasses.
        
        Args:
            raw_input: Raw input string.
            
        Returns:
            Converted value of appropriate type.
        """
        pass
    
    def _handle_timeout(self):
        """Handle timeout if timeout is set."""
        if self.timeout:
            # Timeout handling would be implemented with signal or threading
            # For now, this is a placeholder
            pass
    
    def _handle_interruption(self):
        """Handle user interruption (Ctrl+C, Ctrl+D)."""
        raise InputInterrupted("Input was interrupted by user")
    
    def get(self) -> Any:
        """
        Get input from user with all configured options.
        
        Returns:
            User input value (converted to appropriate type).
            
        Raises:
            InputCancelled: If user cancels input.
            RetryLimitExceeded: If retry limit is exceeded.
            ValidationError: If validation fails after all retries.
        """
        self.retry_handler.reset()
        
        while self.retry_handler.can_retry():
            try:
                # Display prompt
                formatted_prompt = self._format_prompt()
                self.terminal.write(formatted_prompt)
                
                # Read input
                try:
                    raw_input = self._read_input()
                except (KeyboardInterrupt, EOFError):
                    self._handle_interruption()
                    raise InputCancelled()
                
                # Process input
                try:
                    result = self._process_input(raw_input)
                    if result is None:  # Help was displayed, retry
                        continue
                    return result
                except EmptyInputError:
                    if self.default is not None:
                        return self.default
                    if not self.required:
                        return None
                    self.terminal.write(f"Input is required for {self.field_name}\n")
                    self.retry_handler.increment()
                    continue
                except Exception as e:
                    # Validation error or other error
                    self.retry_handler.record_error(e)
                    error_msg = str(e)
                    if self.retry_message:
                        self.terminal.write(f"{self.retry_message}\n")
                    else:
                        self.terminal.write(f"Invalid input: {error_msg}\n")
                    
                    self.retry_handler.increment()
                    if self.retry_handler.can_retry():
                        remaining = self.retry_handler.get_remaining_attempts()
                        self.terminal.write(f"Please try again ({remaining} attempt(s) remaining).\n")
                    continue
            
            except InputCancelled:
                raise
            except Exception as e:
                self.retry_handler.increment()
                if not self.retry_handler.can_retry():
                    raise RetryLimitExceeded(attempts=self.retry_limit)
                continue
        
        raise RetryLimitExceeded(attempts=self.retry_limit)

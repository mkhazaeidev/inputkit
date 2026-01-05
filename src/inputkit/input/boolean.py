"""
boolean.py

This module provides classes for getting boolean and confirmation input from the user.

Provides input handlers for:
- Yes/No confirmation
- True/False input
- Continue confirmation
- Agreement/consent input

All handlers support validators, retry logic, defaults, and help text.

Purpose:
- Allow developers to ask for boolean/confirmation inputs naturally.
- Provide flexible confirmation scenarios.
- Support user-friendly boolean input collection.
"""

from typing import Optional, Pattern

from .core import BaseInputHandler
from ..validators.core import BaseValidator
from ..validators.common import (
    BooleanValidator, YesNoValidator, TrueFalseValidator,
    ContinueConfirmationValidator, AgreementValidator
)


class YesNoInputHandler(BaseInputHandler):
    """
    Handler for Yes/No confirmation input.
    """
    
    def __init__(
        self,
        prompt: str = "Continue? (yes/no)",
        default: Optional[bool] = None,
        validator: Optional[BaseValidator] = None,
        **kwargs
    ):
        """
        Initialize yes/no input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value (True/False).
            validator: Optional custom validator.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = YesNoValidator(field_name=kwargs.get("field_name"))
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read yes/no input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> bool:
        """Convert input to boolean."""
        value = raw_input.strip().lower()
        return value.startswith('y')


class TrueFalseInputHandler(BaseInputHandler):
    """
    Handler for True/False input.
    """
    
    def __init__(
        self,
        prompt: str = "Enter true/false",
        default: Optional[bool] = None,
        validator: Optional[BaseValidator] = None,
        **kwargs
    ):
        """
        Initialize true/false input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value (True/False).
            validator: Optional custom validator.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = TrueFalseValidator(field_name=kwargs.get("field_name"))
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read true/false input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> bool:
        """Convert input to boolean."""
        value = raw_input.strip().lower()
        return value in ('true', 't', '1')


class ContinueConfirmationInputHandler(BaseInputHandler):
    """
    Handler for continue/proceed confirmation input.
    """
    
    def __init__(
        self,
        prompt: str = "Continue?",
        default: Optional[bool] = None,
        validator: Optional[BaseValidator] = None,
        **kwargs
    ):
        """
        Initialize continue confirmation input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value (True/False).
            validator: Optional custom validator.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = ContinueConfirmationValidator(field_name=kwargs.get("field_name"))
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read continue confirmation input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> bool:
        """Convert input to boolean."""
        value = raw_input.strip().lower()
        return value in ('continue', 'proceed', 'yes', 'y', 'ok', 'sure', 'confirm', 'go')


class AgreementInputHandler(BaseInputHandler):
    """
    Handler for agreement/consent input.
    """
    
    def __init__(
        self,
        prompt: str = "Do you agree?",
        default: Optional[bool] = None,
        validator: Optional[BaseValidator] = None,
        **kwargs
    ):
        """
        Initialize agreement input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value (True/False).
            validator: Optional custom validator.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = AgreementValidator(field_name=kwargs.get("field_name"))
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read agreement input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> bool:
        """Convert input to boolean."""
        value = raw_input.strip().lower()
        return value in ('agree', 'accept', 'yes', 'y', 'consent', 'acknowledge', 'ack')


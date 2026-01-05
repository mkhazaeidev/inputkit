"""
numeric.py

This module provides classes for getting numeric input from the user.

Provides input handlers for:
- Integer input (positive, negative, any)
- Float input (positive, negative, any)
- Range-limited number input
- Percentage input
- Year input
- Age input

All handlers support validators, retry logic, defaults, and help text.

Purpose:
- Allow developers to ask for numeric inputs naturally.
- Provide type conversion and validation.
- Support flexible numeric input scenarios.
"""

from typing import Optional, Pattern, Union

from .core import BaseInputHandler
from ..validators.core import BaseValidator
from ..validators.numeric import (
    IntegerValidator, FloatValidator, RangeValidator,
    PercentageValidator, YearValidator, AgeValidator
)


class IntegerInputHandler(BaseInputHandler):
    """
    Handler for integer input.
    
    Supports positive-only, negative-only, or any integer modes.
    """
    
    def __init__(
        self,
        prompt: str = "Enter integer",
        default: Optional[int] = None,
        validator: Optional[BaseValidator] = None,
        positive_only: bool = False,
        negative_only: bool = False,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize integer input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            positive_only: If True, only accept positive integers.
            negative_only: If True, only accept negative integers.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = IntegerValidator(
                positive_only=positive_only,
                negative_only=negative_only,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read integer input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> int:
        """Convert input to integer."""
        return int(raw_input.strip())


class FloatInputHandler(BaseInputHandler):
    """
    Handler for float input.
    
    Supports positive-only, negative-only, or any float modes.
    """
    
    def __init__(
        self,
        prompt: str = "Enter number",
        default: Optional[float] = None,
        validator: Optional[BaseValidator] = None,
        positive_only: bool = False,
        negative_only: bool = False,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize float input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            positive_only: If True, only accept positive floats.
            negative_only: If True, only accept negative floats.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = FloatValidator(
                positive_only=positive_only,
                negative_only=negative_only,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read float input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> float:
        """Convert input to float."""
        return float(raw_input.strip())


class RangeNumberInputHandler(BaseInputHandler):
    """
    Handler for range-limited number input.
    
    Validates that input is within specified min/max bounds.
    """
    
    def __init__(
        self,
        prompt: str = "Enter number",
        default: Optional[Union[int, float]] = None,
        validator: Optional[BaseValidator] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        **kwargs
    ):
        """
        Initialize range number input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            min_value: Minimum allowed value.
            max_value: Maximum allowed value.
            min_inclusive: If True, min_value is inclusive.
            max_inclusive: If True, max_value is inclusive.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = RangeValidator(
                min_value=min_value,
                max_value=max_value,
                min_inclusive=min_inclusive,
                max_inclusive=max_inclusive,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read range number input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> Union[int, float]:
        """Convert input to number (int or float)."""
        value = raw_input.strip()
        try:
            return int(value)
        except ValueError:
            return float(value)


class PercentageInputHandler(BaseInputHandler):
    """
    Handler for percentage input (0-100%).
    """
    
    def __init__(
        self,
        prompt: str = "Enter percentage",
        default: Optional[float] = None,
        validator: Optional[BaseValidator] = None,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize percentage input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = PercentageValidator(
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read percentage input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> float:
        """Convert input to percentage float."""
        value = raw_input.strip().rstrip('%')
        return float(value)


class YearInputHandler(BaseInputHandler):
    """
    Handler for year input (typically 1900-2099).
    """
    
    def __init__(
        self,
        prompt: str = "Enter year",
        default: Optional[int] = None,
        validator: Optional[BaseValidator] = None,
        min_year: int = 1900,
        max_year: int = 2099,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize year input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            min_year: Minimum allowed year.
            max_year: Maximum allowed year.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = YearValidator(
                min_year=min_year,
                max_year=max_year,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read year input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> int:
        """Convert input to year integer."""
        return int(raw_input.strip())


class AgeInputHandler(BaseInputHandler):
    """
    Handler for age input (0-150).
    """
    
    def __init__(
        self,
        prompt: str = "Enter age",
        default: Optional[int] = None,
        validator: Optional[BaseValidator] = None,
        min_age: int = 0,
        max_age: int = 150,
        custom_pattern: Optional[Pattern] = None,
        **kwargs
    ):
        """
        Initialize age input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            min_age: Minimum allowed age.
            max_age: Maximum allowed age.
            custom_pattern: Optional custom regex pattern.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = AgeValidator(
                min_age=min_age,
                max_age=max_age,
                custom_pattern=custom_pattern,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
    
    def _read_input(self) -> str:
        """Read age input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> int:
        """Convert input to age integer."""
        return int(raw_input.strip())

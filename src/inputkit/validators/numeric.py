"""
numeric.py

Validation rules for numeric input in inputkit.

This module provides object-oriented validators for all numeric input types including:
- Integer validation (positive, negative, zero)
- Float validation (positive, negative)
- Range-limited numbers
- Percentage validation
- Year validation (with reasonable bounds)
- Age validation (0-150)

All validators support custom patterns and provide clear error messages.

Purpose:
- Ensure numeric inputs are valid and within expected ranges.
- Keep numeric validation modular and reusable.
- Enable flexible validation with custom constraints.
"""

from typing import Optional, Pattern, Union, Any

from .core import BaseValidator
from .patterns import (
    IntegerPattern, FloatPattern, PercentagePattern, YearPattern, AgePattern
)
from ..exceptions import RangeError, InvalidTypeError, ValidationError


class IntegerValidator(BaseValidator):
    """
    Validator for integer values.
    
    Supports validation of positive, negative, or any integer values.
    Can accept custom regex patterns for specialized integer formats.
    """
    
    def __init__(
        self,
        positive_only: bool = False,
        negative_only: bool = False,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize integer validator.
        
        Args:
            positive_only: If True, only accept positive integers.
            negative_only: If True, only accept negative integers.
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.positive_only = positive_only
        self.negative_only = negative_only
        
        if positive_only and negative_only:
            raise ValueError("Cannot set both positive_only and negative_only to True")
        
        if positive_only:
            self.pattern = IntegerPattern.POSITIVE
        elif negative_only:
            self.pattern = IntegerPattern.NEGATIVE
        else:
            self.pattern = IntegerPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate integer value.
        
        Args:
            value: The value to validate (string or int).
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        # Convert to string if needed
        if isinstance(value, int):
            value_str = str(value)
        elif isinstance(value, str):
            value_str = value
        else:
            self._raise_validation_error(
                f"Expected integer or string, got {type(value).__name__}",
                value=value
            )
        
        pattern = self.custom_pattern or self.pattern
        if not pattern.fullmatch(value_str):
            self._raise_validation_error(
                f"Invalid integer format for {self.field_name or 'field'}",
                value=value
            )
        
        # Additional checks for positive/negative
        try:
            int_val = int(value_str)
            if self.positive_only and int_val <= 0:
                raise RangeError(
                    min_value=1,
                    actual_value=int_val,
                    field=self.field_name,
                    message=f"Integer must be positive for {self.field_name or 'field'}"
                )
            if self.negative_only and int_val >= 0:
                raise RangeError(
                    max_value=-1,
                    actual_value=int_val,
                    field=self.field_name,
                    message=f"Integer must be negative for {self.field_name or 'field'}"
                )
        except ValueError:
            self._raise_validation_error(
                f"Invalid integer value: {value}",
                value=value
            )
        
        return True


class FloatValidator(BaseValidator):
    """
    Validator for floating-point values.
    
    Supports validation of positive, negative, or any float values.
    Can accept custom regex patterns for specialized float formats.
    """
    
    def __init__(
        self,
        positive_only: bool = False,
        negative_only: bool = False,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize float validator.
        
        Args:
            positive_only: If True, only accept positive floats.
            negative_only: If True, only accept negative floats.
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.positive_only = positive_only
        self.negative_only = negative_only
        
        if positive_only and negative_only:
            raise ValueError("Cannot set both positive_only and negative_only to True")
        
        if positive_only:
            self.pattern = FloatPattern.POSITIVE
        elif negative_only:
            self.pattern = FloatPattern.NEGATIVE
        else:
            self.pattern = FloatPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate float value.
        
        Args:
            value: The value to validate (string or float).
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        # Convert to string if needed
        if isinstance(value, float):
            value_str = str(value)
        elif isinstance(value, str):
            value_str = value
        else:
            self._raise_validation_error(
                f"Expected float or string, got {type(value).__name__}",
                value=value
            )
        
        pattern = self.custom_pattern or self.pattern
        if not pattern.fullmatch(value_str):
            self._raise_validation_error(
                f"Invalid float format for {self.field_name or 'field'}",
                value=value
            )
        
        # Additional checks for positive/negative
        try:
            float_val = float(value_str)
            if self.positive_only and float_val <= 0:
                raise RangeError(
                    min_value=0.0,
                    actual_value=float_val,
                    field=self.field_name,
                    message=f"Float must be positive for {self.field_name or 'field'}"
                )
            if self.negative_only and float_val >= 0:
                raise RangeError(
                    max_value=0.0,
                    actual_value=float_val,
                    field=self.field_name,
                    message=f"Float must be negative for {self.field_name or 'field'}"
                )
        except ValueError:
            self._raise_validation_error(
                f"Invalid float value: {value}",
                value=value
            )
        
        return True


class RangeValidator(BaseValidator):
    """
    Validator for numeric values within a specified range.
    
    Works with both integers and floats. Supports inclusive or exclusive bounds.
    """
    
    def __init__(
        self,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        field_name: Optional[str] = None
    ):
        """
        Initialize range validator.
        
        Args:
            min_value: Minimum allowed value (None for no minimum).
            max_value: Maximum allowed value (None for no maximum).
            min_inclusive: If True, min_value is inclusive.
            max_inclusive: If True, max_value is inclusive.
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError("min_value cannot be greater than max_value")
    
    def validate(self, value: Any) -> bool:
        """
        Validate value is within range.
        
        Args:
            value: The numeric value to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        try:
            num_value = float(value) if isinstance(value, str) else value
            if not isinstance(num_value, (int, float)):
                self._raise_validation_error(
                    f"Expected numeric value, got {type(value).__name__}",
                    value=value
                )
        except (ValueError, TypeError):
            self._raise_validation_error(
                f"Invalid numeric value: {value}",
                value=value
            )
        
        if self.min_value is not None:
            if self.min_inclusive:
                if num_value < self.min_value:
                    raise RangeError(
                        min_value=self.min_value,
                        actual_value=num_value,
                        field=self.field_name,
                        message=f"Value must be at least {self.min_value} for {self.field_name or 'field'}"
                    )
            else:
                if num_value <= self.min_value:
                    raise RangeError(
                        min_value=self.min_value,
                        actual_value=num_value,
                        field=self.field_name,
                        message=f"Value must be greater than {self.min_value} for {self.field_name or 'field'}"
                    )
        
        if self.max_value is not None:
            if self.max_inclusive:
                if num_value > self.max_value:
                    raise RangeError(
                        max_value=self.max_value,
                        actual_value=num_value,
                        field=self.field_name,
                        message=f"Value must be at most {self.max_value} for {self.field_name or 'field'}"
                    )
            else:
                if num_value >= self.max_value:
                    raise RangeError(
                        max_value=self.max_value,
                        actual_value=num_value,
                        field=self.field_name,
                        message=f"Value must be less than {self.max_value} for {self.field_name or 'field'}"
                    )
        
        return True


class PercentageValidator(BaseValidator):
    """
    Validator for percentage values (0-100%).
    
    Accepts values with or without the % sign. Supports decimal percentages.
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize percentage validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.pattern = PercentagePattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate percentage value.
        
        Args:
            value: The percentage string to validate.
            
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
            error_message=f"Invalid percentage format for {self.field_name or 'field'}"
        )
        return True


class YearValidator(BaseValidator):
    """
    Validator for year values (typically 1900-2099).
    
    Validates four-digit year strings. Can be extended with custom patterns.
    """
    
    def __init__(
        self,
        min_year: int = 1900,
        max_year: int = 2099,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize year validator.
        
        Args:
            min_year: Minimum allowed year.
            max_year: Maximum allowed year.
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.min_year = min_year
        self.max_year = max_year
        self.pattern = YearPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate year value.
        
        Args:
            value: The year string or integer to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if isinstance(value, int):
            value_str = str(value)
        elif isinstance(value, str):
            value_str = value
        else:
            self._raise_validation_error(
                f"Expected year (int or string), got {type(value).__name__}",
                value=value
            )
        
        pattern = self.custom_pattern or self.pattern
        if not pattern.fullmatch(value_str):
            self._raise_validation_error(
                f"Invalid year format for {self.field_name or 'field'}",
                value=value
            )
        
        try:
            year = int(value_str)
            if year < self.min_year or year > self.max_year:
                raise RangeError(
                    min_value=self.min_year,
                    max_value=self.max_year,
                    actual_value=year,
                    field=self.field_name,
                    message=f"Year must be between {self.min_year} and {self.max_year}"
                )
        except ValueError:
            self._raise_validation_error(
                f"Invalid year value: {value}",
                value=value
            )
        
        return True


class AgeValidator(BaseValidator):
    """
    Validator for age values (0-150).
    
    Validates age strings and ensures they're within reasonable human age bounds.
    """
    
    def __init__(
        self,
        min_age: int = 0,
        max_age: int = 150,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize age validator.
        
        Args:
            min_age: Minimum allowed age (default: 0).
            max_age: Maximum allowed age (default: 150).
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.min_age = min_age
        self.max_age = max_age
        self.pattern = AgePattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate age value.
        
        Args:
            value: The age string or integer to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if isinstance(value, int):
            value_str = str(value)
        elif isinstance(value, str):
            value_str = value
        else:
            self._raise_validation_error(
                f"Expected age (int or string), got {type(value).__name__}",
                value=value
            )
        
        pattern = self.custom_pattern or self.pattern
        if not pattern.fullmatch(value_str):
            self._raise_validation_error(
                f"Invalid age format for {self.field_name or 'field'}",
                value=value
            )
        
        try:
            age = int(value_str)
            if age < self.min_age or age > self.max_age:
                raise RangeError(
                    min_value=self.min_age,
                    max_value=self.max_age,
                    actual_value=age,
                    field=self.field_name,
                    message=f"Age must be between {self.min_age} and {self.max_age}"
                )
        except ValueError:
            self._raise_validation_error(
                f"Invalid age value: {value}",
                value=value
            )
        
        return True

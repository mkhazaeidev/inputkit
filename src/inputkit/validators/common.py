"""
common.py

Generic validators that can apply to any type of input in inputkit.

This module provides:
- Required/optional value validation
- Boolean and confirmation input validation (Yes/No, True/False, etc.)
- Nullable/not-null checks
- Empty value checks

These validators are reusable across text, numeric, pattern, or security validations.

Purpose:
- Reduce code duplication.
- Provide common building blocks for all validation logic.
- Enable flexible validation workflows.
"""

import re
from typing import Any, Optional, Pattern

from .core import BaseValidator
from .patterns import BooleanPattern
from ..exceptions import RequiredValueError, ValidationError


class RequiredValidator(BaseValidator):
    """
    Validator that ensures a value is provided (not None or empty).
    
    Can be used with any input type to enforce required fields.
    """
    
    def __init__(self, field_name: Optional[str] = None):
        """
        Initialize required validator.
        
        Args:
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
    
    def validate(self, value: Any) -> bool:
        """
        Validate that value is provided.
        
        Args:
            value: The value to validate.
            
        Returns:
            True if value is provided.
            
        Raises:
            RequiredValueError: If value is None or empty.
        """
        if value is None:
            raise RequiredValueError(field=self.field_name)
        
        if isinstance(value, str) and not value.strip():
            raise RequiredValueError(field=self.field_name)
        
        if isinstance(value, (list, dict, tuple, set)) and len(value) == 0:
            raise RequiredValueError(field=self.field_name)
        
        return True


class OptionalValidator(BaseValidator):
    """
    Validator that allows None or empty values.
    
    Useful for optional fields - always passes if value is None/empty,
    otherwise delegates to another validator.
    """
    
    def __init__(self, inner_validator: Optional[BaseValidator] = None, field_name: Optional[str] = None):
        """
        Initialize optional validator.
        
        Args:
            inner_validator: Optional validator to apply if value is provided.
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.inner_validator = inner_validator
    
    def validate(self, value: Any) -> bool:
        """
        Validate value (always passes if None/empty, otherwise uses inner validator).
        
        Args:
            value: The value to validate.
            
        Returns:
            True if value is None/empty or passes inner validation.
            
        Raises:
            ValidationError: If inner validator fails.
        """
        # Always pass if value is None or empty
        if value is None:
            return True
        
        if isinstance(value, str) and not value.strip():
            return True
        
        if isinstance(value, (list, dict, tuple, set)) and len(value) == 0:
            return True
        
        # If value is provided and inner validator exists, use it
        if self.inner_validator:
            return self.inner_validator.validate(value)
        
        return True


class BooleanValidator(BaseValidator):
    """
    Validator for boolean and confirmation inputs.
    
    Accepts various formats: yes/no, y/n, true/false, t/f, 1/0, on/off, etc.
    Supports custom patterns for specialized confirmation formats.
    """
    
    def __init__(
        self,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize boolean validator.
        
        Args:
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.pattern = BooleanPattern.PATTERN
    
    def validate(self, value: Any) -> bool:
        """
        Validate boolean/confirmation input.
        
        Args:
            value: The boolean string or boolean value to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        # Accept Python bool directly
        if isinstance(value, bool):
            return True
        
        if not isinstance(value, str):
            value = str(value).lower()
        else:
            value = value.lower().strip()
        
        pattern = self.custom_pattern or self.pattern
        self._match_pattern(
            value,
            pattern,
            error_message=f"Invalid boolean/confirmation format for {self.field_name or 'field'}"
        )
        return True


class YesNoValidator(BaseValidator):
    """
    Validator specifically for Yes/No confirmation inputs.
    
    More restrictive than BooleanValidator - only accepts yes/no variations.
    """
    
    def __init__(self, field_name: Optional[str] = None):
        """
        Initialize yes/no validator.
        
        Args:
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.pattern = re.compile(r"^(?i)(y(es)?|no?)$")
    
    def validate(self, value: Any) -> bool:
        """
        Validate yes/no input.
        
        Args:
            value: The yes/no string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, str):
            value = str(value)
        
        self._match_pattern(
            value,
            self.pattern,
            error_message=f"Must be 'yes' or 'no' for {self.field_name or 'field'}"
        )
        return True


class TrueFalseValidator(BaseValidator):
    """
    Validator specifically for True/False inputs.
    
    Only accepts true/false variations (not yes/no).
    """
    
    def __init__(self, field_name: Optional[str] = None):
        """
        Initialize true/false validator.
        
        Args:
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.pattern = re.compile(r"^(?i)(true|false|t|f|1|0)$")
    
    def validate(self, value: Any) -> bool:
        """
        Validate true/false input.
        
        Args:
            value: The true/false string or boolean to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if isinstance(value, bool):
            return True
        
        if not isinstance(value, str):
            value = str(value)
        
        self._match_pattern(
            value,
            self.pattern,
            error_message=f"Must be 'true' or 'false' for {self.field_name or 'field'}"
        )
        return True


class ContinueConfirmationValidator(BaseValidator):
    """
    Validator for continue/confirmation prompts.
    
    Accepts: continue, proceed, yes, ok, sure, etc.
    """
    
    def __init__(self, field_name: Optional[str] = None):
        """
        Initialize continue confirmation validator.
        
        Args:
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.pattern = re.compile(r"^(?i)(continue|proceed|yes|y|ok|sure|confirm|go)$")
    
    def validate(self, value: Any) -> bool:
        """
        Validate continue confirmation input.
        
        Args:
            value: The confirmation string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, str):
            value = str(value)
        
        self._match_pattern(
            value,
            self.pattern,
            error_message=f"Invalid confirmation for {self.field_name or 'field'}"
        )
        return True


class AgreementValidator(BaseValidator):
    """
    Validator for agreement/consent inputs.
    
    Accepts: agree, accept, yes, consent, etc.
    """
    
    def __init__(self, field_name: Optional[str] = None):
        """
        Initialize agreement validator.
        
        Args:
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.pattern = re.compile(r"^(?i)(agree|accept|yes|y|consent|acknowledge|ack)$")
    
    def validate(self, value: Any) -> bool:
        """
        Validate agreement input.
        
        Args:
            value: The agreement string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, str):
            value = str(value)
        
        self._match_pattern(
            value,
            self.pattern,
            error_message=f"Agreement required for {self.field_name or 'field'}"
        )
        return True

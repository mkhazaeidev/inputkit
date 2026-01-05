"""
composite.py

Validators for structured/composite inputs and selection inputs in inputkit.

This module provides:
- Credentials validation (username + password)
- Address validation (country, city, postal code)
- Phone number validation (with country code support)
- Date range validation
- Multi-field form validation
- Single choice selection validation
- Multiple choice selection validation
- Indexed list selection validation
- Enum-based selection validation

Purpose:
- Handle complex, multi-field validation scenarios.
- Provide reusable validators for structured data.
- Enable flexible validation of composite inputs.
"""

import re
from typing import Optional, Pattern, Any, List, Dict, Union, Set
from enum import Enum
from datetime import datetime, date

from .core import BaseValidator
from .strings import UsernameValidator, EmailValidator
from .security import PasswordValidator
from .patterns import MobileNumberPattern
from ..exceptions import ValidationError, RequiredValueError, PatternMismatchError


class CredentialsValidator(BaseValidator):
    """
    Validator for credentials (username + password combination).
    
    Validates both username and password fields together, ensuring both meet requirements.
    """
    
    def __init__(
        self,
        username_validator: Optional[BaseValidator] = None,
        password_validator: Optional[BaseValidator] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize credentials validator.
        
        Args:
            username_validator: Optional custom username validator (default: UsernameValidator).
            password_validator: Optional custom password validator (default: PasswordValidator).
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.username_validator = username_validator or UsernameValidator(field_name="username")
        self.password_validator = password_validator or PasswordValidator(field_name="password")
    
    def validate(self, value: Any) -> bool:
        """
        Validate credentials (dict with 'username' and 'password' keys).
        
        Args:
            value: Dictionary with 'username' and 'password' keys.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, dict):
            self._raise_validation_error(
                f"Expected dict with 'username' and 'password', got {type(value).__name__}",
                value=value
            )
        
        if 'username' not in value:
            raise RequiredValueError(field="username")
        
        if 'password' not in value:
            raise RequiredValueError(field="password")
        
        self.username_validator.validate(value['username'])
        self.password_validator.validate(value['password'])
        
        return True


class AddressValidator(BaseValidator):
    """
    Validator for address information (country, city, postal code).
    
    Validates structured address data with optional fields.
    """
    
    def __init__(
        self,
        require_country: bool = True,
        require_city: bool = True,
        require_postal_code: bool = False,
        country_pattern: Optional[Pattern] = None,
        city_pattern: Optional[Pattern] = None,
        postal_code_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize address validator.
        
        Args:
            require_country: Require country field.
            require_city: Require city field.
            require_postal_code: Require postal code field.
            country_pattern: Optional custom regex for country.
            city_pattern: Optional custom regex for city.
            postal_code_pattern: Optional custom regex for postal code.
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.require_country = require_country
        self.require_city = require_city
        self.require_postal_code = require_postal_code
        self.country_pattern = country_pattern or re.compile(r"^[A-Za-z\s]{2,50}$")
        self.city_pattern = city_pattern or re.compile(r"^[A-Za-z\s-']{2,50}$")
        self.postal_code_pattern = postal_code_pattern or re.compile(r"^[A-Za-z0-9\s-]{3,10}$")
    
    def validate(self, value: Any) -> bool:
        """
        Validate address (dict with 'country', 'city', 'postal_code' keys).
        
        Args:
            value: Dictionary with address fields.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, dict):
            self._raise_validation_error(
                f"Expected dict with address fields, got {type(value).__name__}",
                value=value
            )
        
        if self.require_country:
            if 'country' not in value or not value['country']:
                raise RequiredValueError(field="country")
            if not self.country_pattern.fullmatch(value['country']):
                raise PatternMismatchError(pattern=str(self.country_pattern.pattern), value=value['country'], field="country")
        
        if self.require_city:
            if 'city' not in value or not value['city']:
                raise RequiredValueError(field="city")
            if not self.city_pattern.fullmatch(value['city']):
                raise PatternMismatchError(pattern=str(self.city_pattern.pattern), value=value['city'], field="city")
        
        if self.require_postal_code:
            if 'postal_code' not in value or not value['postal_code']:
                raise RequiredValueError(field="postal_code")
            if not self.postal_code_pattern.fullmatch(value['postal_code']):
                raise PatternMismatchError(pattern=str(self.postal_code_pattern.pattern), value=value['postal_code'], field="postal_code")
        
        return True


class PhoneNumberValidator(BaseValidator):
    """
    Validator for phone numbers with country code support.
    
    Uses MobileNumberPattern for validation with country-specific rules.
    """
    
    def __init__(
        self,
        country: Optional[str] = None,
        custom_pattern: Optional[Pattern] = None,
        field_name: Optional[str] = None
    ):
        """
        Initialize phone number validator.
        
        Args:
            country: Optional country code (e.g., 'IR', 'US', 'UK').
            custom_pattern: Optional custom regex pattern.
            field_name: Optional field name for error messages.
        """
        super().__init__(custom_pattern=custom_pattern, field_name=field_name)
        self.country = country
    
    def validate(self, value: Any) -> bool:
        """
        Validate phone number.
        
        Args:
            value: The phone number string to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, str):
            value = str(value)
        
        if self.custom_pattern:
            self._match_pattern(value, self.custom_pattern)
        else:
            if not MobileNumberPattern.is_valid(value, country=self.country):
                self._raise_validation_error(
                    f"Invalid phone number format for {self.field_name or 'field'}",
                    value=value
                )
        
        return True


class DateRangeValidator(BaseValidator):
    """
    Validator for date ranges (start date and end date).
    
    Ensures end date is after start date and validates date formats.
    """
    
    def __init__(
        self,
        date_format: str = "%Y-%m-%d",
        allow_same_date: bool = False,
        field_name: Optional[str] = None
    ):
        """
        Initialize date range validator.
        
        Args:
            date_format: Date format string (default: YYYY-MM-DD).
            allow_same_date: If True, allow start and end dates to be the same.
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.date_format = date_format
        self.allow_same_date = allow_same_date
    
    def validate(self, value: Any) -> bool:
        """
        Validate date range (dict with 'start_date' and 'end_date' keys).
        
        Args:
            value: Dictionary with 'start_date' and 'end_date' strings.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, dict):
            self._raise_validation_error(
                f"Expected dict with 'start_date' and 'end_date', got {type(value).__name__}",
                value=value
            )
        
        if 'start_date' not in value:
            raise RequiredValueError(field="start_date")
        
        if 'end_date' not in value:
            raise RequiredValueError(field="end_date")
        
        try:
            start = datetime.strptime(value['start_date'], self.date_format).date()
            end = datetime.strptime(value['end_date'], self.date_format).date()
        except ValueError as e:
            self._raise_validation_error(
                f"Invalid date format. Expected {self.date_format}",
                value=value
            )
        
        if end < start:
            self._raise_validation_error(
                "End date must be after start date",
                value=value
            )
        
        if not self.allow_same_date and end == start:
            self._raise_validation_error(
                "Start date and end date cannot be the same",
                value=value
            )
        
        return True


class SingleChoiceValidator(BaseValidator):
    """
    Validator for single choice selection from a list of options.
    
    Ensures the selected value is one of the allowed choices.
    """
    
    def __init__(
        self,
        choices: List[Any],
        case_sensitive: bool = True,
        field_name: Optional[str] = None
    ):
        """
        Initialize single choice validator.
        
        Args:
            choices: List of allowed choices.
            case_sensitive: If False, comparison is case-insensitive for strings.
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.choices = choices
        self.case_sensitive = case_sensitive
    
    def validate(self, value: Any) -> bool:
        """
        Validate single choice selection.
        
        Args:
            value: The selected value.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not self.choices:
            self._raise_validation_error("No choices available", value=value)
        
        if self.case_sensitive:
            if value not in self.choices:
                self._raise_validation_error(
                    f"Value must be one of: {', '.join(map(str, self.choices))}",
                    value=value
                )
        else:
            if isinstance(value, str):
                choices_lower = [str(c).lower() for c in self.choices]
                if value.lower() not in choices_lower:
                    self._raise_validation_error(
                        f"Value must be one of: {', '.join(map(str, self.choices))}",
                        value=value
                    )
            else:
                if value not in self.choices:
                    self._raise_validation_error(
                        f"Value must be one of: {', '.join(map(str, self.choices))}",
                        value=value
                    )
        
        return True


class MultipleChoiceValidator(BaseValidator):
    """
    Validator for multiple choice selection from a list of options.
    
    Ensures all selected values are from the allowed choices.
    """
    
    def __init__(
        self,
        choices: List[Any],
        min_selections: int = 1,
        max_selections: Optional[int] = None,
        case_sensitive: bool = True,
        field_name: Optional[str] = None
    ):
        """
        Initialize multiple choice validator.
        
        Args:
            choices: List of allowed choices.
            min_selections: Minimum number of selections required.
            max_selections: Maximum number of selections allowed (None for no limit).
            case_sensitive: If False, comparison is case-insensitive for strings.
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.choices = choices
        self.min_selections = min_selections
        self.max_selections = max_selections
        self.case_sensitive = case_sensitive
    
    def validate(self, value: Any) -> bool:
        """
        Validate multiple choice selection (list of values).
        
        Args:
            value: List of selected values.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, (list, tuple, set)):
            self._raise_validation_error(
                f"Expected list/tuple/set, got {type(value).__name__}",
                value=value
            )
        
        selections = list(value)
        
        if len(selections) < self.min_selections:
            self._raise_validation_error(
                f"At least {self.min_selections} selection(s) required",
                value=value
            )
        
        if self.max_selections and len(selections) > self.max_selections:
            self._raise_validation_error(
                f"At most {self.max_selections} selection(s) allowed",
                value=value
            )
        
        for selection in selections:
            if self.case_sensitive:
                if selection not in self.choices:
                    self._raise_validation_error(
                        f"Invalid choice: {selection}. Must be one of: {', '.join(map(str, self.choices))}",
                        value=value
                    )
            else:
                if isinstance(selection, str):
                    choices_lower = [str(c).lower() for c in self.choices]
                    if selection.lower() not in choices_lower:
                        self._raise_validation_error(
                            f"Invalid choice: {selection}. Must be one of: {', '.join(map(str, self.choices))}",
                            value=value
                        )
                else:
                    if selection not in self.choices:
                        self._raise_validation_error(
                            f"Invalid choice: {selection}. Must be one of: {', '.join(map(str, self.choices))}",
                            value=value
                        )
        
        return True


class IndexedListValidator(BaseValidator):
    """
    Validator for indexed list selection (selection by index number).
    
    Validates that the selected index is within the valid range.
    """
    
    def __init__(
        self,
        max_index: int,
        min_index: int = 0,
        field_name: Optional[str] = None
    ):
        """
        Initialize indexed list validator.
        
        Args:
            max_index: Maximum valid index (exclusive).
            min_index: Minimum valid index (default: 0).
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        self.max_index = max_index
        self.min_index = min_index
    
    def validate(self, value: Any) -> bool:
        """
        Validate indexed selection.
        
        Args:
            value: The index value (int or string representation).
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        try:
            index = int(value)
        except (ValueError, TypeError):
            self._raise_validation_error(
                f"Expected integer index, got {type(value).__name__}",
                value=value
            )
        
        if index < self.min_index or index >= self.max_index:
            self._raise_validation_error(
                f"Index must be between {self.min_index} and {self.max_index - 1}",
                value=value
            )
        
        return True


class EnumValidator(BaseValidator):
    """
    Validator for enum-based selection.
    
    Validates that the value is a valid member of the provided enum.
    """
    
    def __init__(
        self,
        enum_class: type,
        field_name: Optional[str] = None
    ):
        """
        Initialize enum validator.
        
        Args:
            enum_class: The enum class to validate against.
            field_name: Optional field name for error messages.
        """
        super().__init__(field_name=field_name)
        if not issubclass(enum_class, Enum):
            raise ValueError("enum_class must be a subclass of Enum")
        self.enum_class = enum_class
    
    def validate(self, value: Any) -> bool:
        """
        Validate enum value.
        
        Args:
            value: The value to validate (can be enum member, name, or value).
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        # Check if value is already an enum member
        if isinstance(value, self.enum_class):
            return True
        
        # Try to match by name
        try:
            if isinstance(value, str):
                self.enum_class[value]
                return True
        except KeyError:
            pass
        
        # Try to match by value
        try:
            self.enum_class(value)
            return True
        except ValueError:
            pass
        
        self._raise_validation_error(
            f"Value must be one of {[e.name for e in self.enum_class]}: {value}",
            value=value
        )


class MultiFieldFormValidator(BaseValidator):
    """
    Validator for multi-field forms.
    
    Validates a dictionary of fields using individual validators for each field.
    """
    
    def __init__(
        self,
        field_validators: Dict[str, BaseValidator],
        require_all: bool = True,
        field_name: Optional[str] = None
    ):
        """
        Initialize multi-field form validator.
        
        Args:
            field_validators: Dictionary mapping field names to their validators.
            require_all: If True, all fields are required. If False, only validate provided fields.
            field_name: Optional form name for error messages.
        """
        super().__init__(field_name=field_name)
        self.field_validators = field_validators
        self.require_all = require_all
    
    def validate(self, value: Any) -> bool:
        """
        Validate multi-field form (dict of field values).
        
        Args:
            value: Dictionary with field names as keys and values to validate.
            
        Returns:
            True if validation passes.
            
        Raises:
            ValidationError: If validation fails.
        """
        if not isinstance(value, dict):
            self._raise_validation_error(
                f"Expected dict with form fields, got {type(value).__name__}",
                value=value
            )
        
        errors = []
        
        for field_name, validator in self.field_validators.items():
            if self.require_all and field_name not in value:
                errors.append(RequiredValueError(field=field_name))
            elif field_name in value:
                try:
                    validator.validate(value[field_name])
                except ValidationError as e:
                    errors.append(e)
        
        if errors:
            from ..exceptions import MultiValidationError
            raise MultiValidationError(errors)
        
        return True


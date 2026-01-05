"""
composite.py

This module provides classes for getting structured/composite input from the user.

Provides input handlers for:
- Credentials (username + password)
- Address (country, city, postal code)
- Phone number (with country code)
- Date ranges (start/end dates)
- Multi-field forms

All handlers support validators, retry logic, defaults, and help text.

Purpose:
- Handle complex, multi-field input scenarios.
- Provide structured data collection.
- Support validation of composite inputs.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime

from .core import BaseInputHandler
from .text import UsernameInputHandler
from .secure import PasswordInputHandler
from .numeric import IntegerInputHandler
from ..validators.core import BaseValidator
from ..validators.composite import (
    CredentialsValidator, AddressValidator, PhoneNumberValidator,
    DateRangeValidator, MultiFieldFormValidator
)
from ..exceptions import InputCancelled


class CredentialsInputHandler(BaseInputHandler):
    """
    Handler for credentials input (username + password).
    
    Prompts for both username and password sequentially.
    """
    
    def __init__(
        self,
        prompt: str = "Enter credentials",
        default: Optional[Dict[str, str]] = None,
        validator: Optional[BaseValidator] = None,
        username_prompt: str = "Username",
        password_prompt: str = "Password",
        **kwargs
    ):
        """
        Initialize credentials input handler.
        
        Args:
            prompt: Main prompt text.
            default: Default credentials dict with 'username' and 'password' keys.
            validator: Optional custom validator.
            username_prompt: Prompt for username field.
            password_prompt: Prompt for password field.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = CredentialsValidator(field_name=kwargs.get("field_name"))
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.username_prompt = username_prompt
        self.password_prompt = password_prompt
    
    def _read_input(self) -> str:
        """Read credentials input (not used directly, handled in get())."""
        # This is handled differently - we prompt for each field
        return ""
    
    def _convert_value(self, raw_input: str) -> Dict[str, str]:
        """Convert input to credentials dict."""
        # This is handled in get() method
        return {}
    
    def get(self) -> Dict[str, str]:
        """
        Get credentials from user.
        
        Returns:
            Dictionary with 'username' and 'password' keys.
        """
        username_handler = UsernameInputHandler(
            prompt=self.username_prompt,
            default=self.default.get('username') if self.default else None,
            field_name="username",
            retry_limit=self.retry_limit,
            required=True
        )
        
        password_handler = PasswordInputHandler(
            prompt=self.password_prompt,
            default=self.default.get('password') if self.default else None,
            field_name="password",
            retry_limit=self.retry_limit,
            required=True
        )
        
        username = username_handler.get()
        password = password_handler.get()
        
        credentials = {"username": username, "password": password}
        
        # Validate if validator provided
        if self.validator:
            self.validator.validate(credentials)
        
        return credentials


class AddressInputHandler(BaseInputHandler):
    """
    Handler for address input (country, city, postal code).
    
    Prompts for address fields sequentially.
    """
    
    def __init__(
        self,
        prompt: str = "Enter address",
        default: Optional[Dict[str, str]] = None,
        validator: Optional[BaseValidator] = None,
        require_country: bool = True,
        require_city: bool = True,
        require_postal_code: bool = False,
        **kwargs
    ):
        """
        Initialize address input handler.
        
        Args:
            prompt: Main prompt text.
            default: Default address dict.
            validator: Optional custom validator.
            require_country: Require country field.
            require_city: Require city field.
            require_postal_code: Require postal code field.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = AddressValidator(
                require_country=require_country,
                require_city=require_city,
                require_postal_code=require_postal_code,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.require_country = require_country
        self.require_city = require_city
        self.require_postal_code = require_postal_code
    
    def _read_input(self) -> str:
        """Read address input (not used directly)."""
        return ""
    
    def _convert_value(self, raw_input: str) -> Dict[str, str]:
        """Convert input to address dict."""
        return {}
    
    def get(self) -> Dict[str, str]:
        """
        Get address from user.
        
        Returns:
            Dictionary with address fields.
        """
        from .text import PlainTextInputHandler
        
        address = {}
        
        if self.require_country:
            country_handler = PlainTextInputHandler(
                prompt="Country",
                default=self.default.get('country') if self.default else None,
                field_name="country",
                retry_limit=self.retry_limit,
                required=True
            )
            address['country'] = country_handler.get()
        
        if self.require_city:
            city_handler = PlainTextInputHandler(
                prompt="City",
                default=self.default.get('city') if self.default else None,
                field_name="city",
                retry_limit=self.retry_limit,
                required=True
            )
            address['city'] = city_handler.get()
        
        if self.require_postal_code:
            postal_handler = PlainTextInputHandler(
                prompt="Postal code",
                default=self.default.get('postal_code') if self.default else None,
                field_name="postal_code",
                retry_limit=self.retry_limit,
                required=True
            )
            address['postal_code'] = postal_handler.get()
        
        # Validate if validator provided
        if self.validator:
            self.validator.validate(address)
        
        return address


class PhoneNumberInputHandler(BaseInputHandler):
    """
    Handler for phone number input with country support.
    """
    
    def __init__(
        self,
        prompt: str = "Enter phone number",
        default: Optional[str] = None,
        validator: Optional[BaseValidator] = None,
        country: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize phone number input handler.
        
        Args:
            prompt: Prompt text.
            default: Default value.
            validator: Optional custom validator.
            country: Optional country code (e.g., 'IR', 'US', 'UK').
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = PhoneNumberValidator(
                country=country,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.country = country
    
    def _read_input(self) -> str:
        """Read phone number input."""
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        """Convert input to phone number string."""
        return raw_input.strip()


class DateRangeInputHandler(BaseInputHandler):
    """
    Handler for date range input (start date and end date).
    
    Prompts for start and end dates sequentially.
    """
    
    def __init__(
        self,
        prompt: str = "Enter date range",
        default: Optional[Dict[str, str]] = None,
        validator: Optional[BaseValidator] = None,
        date_format: str = "%Y-%m-%d",
        allow_same_date: bool = False,
        **kwargs
    ):
        """
        Initialize date range input handler.
        
        Args:
            prompt: Main prompt text.
            default: Default date range dict with 'start_date' and 'end_date'.
            validator: Optional custom validator.
            date_format: Date format string (default: YYYY-MM-DD).
            allow_same_date: If True, allow start and end dates to be the same.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = DateRangeValidator(
                date_format=date_format,
                allow_same_date=allow_same_date,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.date_format = date_format
        self.allow_same_date = allow_same_date
    
    def _read_input(self) -> str:
        """Read date range input (not used directly)."""
        return ""
    
    def _convert_value(self, raw_input: str) -> Dict[str, str]:
        """Convert input to date range dict."""
        return {}
    
    def get(self) -> Dict[str, str]:
        """
        Get date range from user.
        
        Returns:
            Dictionary with 'start_date' and 'end_date' keys.
        """
        from .text import PlainTextInputHandler
        
        start_handler = PlainTextInputHandler(
            prompt=f"Start date ({self.date_format})",
            default=self.default.get('start_date') if self.default else None,
            field_name="start_date",
            retry_limit=self.retry_limit,
            required=True,
            hint=f"Format: {self.date_format}"
        )
        
        end_handler = PlainTextInputHandler(
            prompt=f"End date ({self.date_format})",
            default=self.default.get('end_date') if self.default else None,
            field_name="end_date",
            retry_limit=self.retry_limit,
            required=True,
            hint=f"Format: {self.date_format}"
        )
        
        start_date = start_handler.get()
        end_date = end_handler.get()
        
        date_range = {"start_date": start_date, "end_date": end_date}
        
        # Validate if validator provided
        if self.validator:
            self.validator.validate(date_range)
        
        return date_range


class MultiFieldFormInputHandler(BaseInputHandler):
    """
    Handler for multi-field form input.
    
    Prompts for multiple fields using individual input handlers.
    """
    
    def __init__(
        self,
        field_handlers: Dict[str, BaseInputHandler],
        prompt: str = "Fill in the form",
        default: Optional[Dict[str, Any]] = None,
        validator: Optional[BaseValidator] = None,
        require_all: bool = True,
        **kwargs
    ):
        """
        Initialize multi-field form input handler.
        
        Args:
            field_handlers: Dictionary mapping field names to their input handlers.
            prompt: Main prompt text.
            default: Default form values dict.
            validator: Optional custom validator.
            require_all: If True, all fields are required.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            # Create validators from handlers
            field_validators = {}
            for field_name, handler in field_handlers.items():
                if handler.validator:
                    field_validators[field_name] = handler.validator
            
            if field_validators:
                validator = MultiFieldFormValidator(
                    field_validators=field_validators,
                    require_all=require_all,
                    field_name=kwargs.get("field_name")
                )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.field_handlers = field_handlers
        self.require_all = require_all
    
    def _read_input(self) -> str:
        """Read form input (not used directly)."""
        return ""
    
    def _convert_value(self, raw_input: str) -> Dict[str, Any]:
        """Convert input to form dict."""
        return {}
    
    def get(self) -> Dict[str, Any]:
        """
        Get form data from user.
        
        Returns:
            Dictionary with form field values.
        """
        form_data = {}
        
        self.terminal.write(f"\n{self.prompt}:\n\n")
        
        for field_name, handler in self.field_handlers.items():
            # Set default if provided
            if self.default and field_name in self.default:
                handler.default = self.default[field_name]
            
            # Set retry limit
            handler.retry_limit = self.retry_limit
            
            # Get field value
            try:
                form_data[field_name] = handler.get()
            except Exception as e:
                if not self.require_all:
                    continue
                raise
        
        # Validate if validator provided
        if self.validator:
            self.validator.validate(form_data)
        
        return form_data


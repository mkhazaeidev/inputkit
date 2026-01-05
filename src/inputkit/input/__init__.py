"""
input/__init__.py

Public API for all input handlers in inputkit.

This module provides a clean, flat interface to all input handlers organized by category:

Textual Inputs:
    - PlainTextInputHandler: Plain text with length constraints
    - UsernameInputHandler: Usernames and identifiers
    - FullNameInputHandler: Full names (multilingual)
    - EmailInputHandler: Email addresses
    - URLInputHandler: URLs (HTTP, HTTPS, FTP, file)
    - FilePathInputHandler: File paths (Unix/Windows)
    - CommandInputHandler: CLI command strings
    - MultiLineTextInputHandler: Multiline text input
    - SlugInputHandler: URL-friendly slugs

Numeric Inputs:
    - IntegerInputHandler: Integers (positive, negative, any)
    - FloatInputHandler: Floats (positive, negative, any)
    - RangeNumberInputHandler: Range-limited numbers
    - PercentageInputHandler: Percentage values (0-100%)
    - YearInputHandler: Year values (1900-2099)
    - AgeInputHandler: Age values (0-150)

Boolean & Confirmation:
    - YesNoInputHandler: Yes/No confirmations
    - TrueFalseInputHandler: True/False inputs
    - ContinueConfirmationInputHandler: Continue/proceed confirmations
    - AgreementInputHandler: Agreement/consent inputs

Selection Inputs:
    - SingleChoiceInputHandler: Single choice from list
    - MultipleChoiceInputHandler: Multiple choices from list
    - IndexedListInputHandler: Selection by index
    - EnumChoiceInputHandler: Enum-based selection

Security & Sensitive:
    - PasswordInputHandler: Password input (hidden)
    - PinInputHandler: PIN input (hidden)
    - ApiKeyInputHandler: API key input (hidden)
    - TokenInputHandler: Token input (hidden)
    - SecretTextInputHandler: Secret text input (hidden)

Structured/Composite:
    - CredentialsInputHandler: Username + password
    - AddressInputHandler: Country, city, postal code
    - PhoneNumberInputHandler: Phone numbers with country support
    - DateRangeInputHandler: Date ranges (start/end)
    - MultiFieldFormInputHandler: Multi-field form input

Core:
    - BaseInputHandler: Base class for all input handlers

All handlers support:
- Custom validators (pass validator parameter)
- Retry logic with configurable limits
- Default values
- Optional inputs (required=False)
- Help text and hints
- Timeout support
- Cancellation handling (Ctrl+C, Ctrl+D)

Usage Example:
    from inputkit.input import PlainTextInputHandler
    from inputkit.validators import EmailValidator
    
    handler = PlainTextInputHandler(
        prompt="Enter your email",
        validator=EmailValidator(),
        retry_limit=3,
        help_text="Enter a valid email address"
    )
    email = handler.get()

Purpose:
- Hide internal module structure from end-users.
- Make the input package simple and intuitive to use.
- Provide a comprehensive input toolkit for all input types.
"""

# Core
from .core import BaseInputHandler

# Textual inputs
from .text import (
    PlainTextInputHandler,
    UsernameInputHandler,
    FullNameInputHandler,
    EmailInputHandler,
    URLInputHandler,
    FilePathInputHandler,
    CommandInputHandler,
    MultiLineTextInputHandler,
    SlugInputHandler,
)

# Numeric inputs
from .numeric import (
    IntegerInputHandler,
    FloatInputHandler,
    RangeNumberInputHandler,
    PercentageInputHandler,
    YearInputHandler,
    AgeInputHandler,
)

# Boolean/confirmation inputs
from .boolean import (
    YesNoInputHandler,
    TrueFalseInputHandler,
    ContinueConfirmationInputHandler,
    AgreementInputHandler,
)

# Selection inputs
from .choices import (
    SingleChoiceInputHandler,
    MultipleChoiceInputHandler,
    IndexedListInputHandler,
    EnumChoiceInputHandler,
)

# Security/sensitive inputs
from .secure import (
    PasswordInputHandler,
    PinInputHandler,
    ApiKeyInputHandler,
    TokenInputHandler,
    SecretTextInputHandler,
)

# Composite/structured inputs
from .composite import (
    CredentialsInputHandler,
    AddressInputHandler,
    PhoneNumberInputHandler,
    DateRangeInputHandler,
    MultiFieldFormInputHandler,
)

__all__ = [
    # Core
    "BaseInputHandler",
    # Textual
    "PlainTextInputHandler",
    "UsernameInputHandler",
    "FullNameInputHandler",
    "EmailInputHandler",
    "URLInputHandler",
    "FilePathInputHandler",
    "CommandInputHandler",
    "MultiLineTextInputHandler",
    "SlugInputHandler",
    # Numeric
    "IntegerInputHandler",
    "FloatInputHandler",
    "RangeNumberInputHandler",
    "PercentageInputHandler",
    "YearInputHandler",
    "AgeInputHandler",
    # Boolean/Confirmation
    "YesNoInputHandler",
    "TrueFalseInputHandler",
    "ContinueConfirmationInputHandler",
    "AgreementInputHandler",
    # Selection
    "SingleChoiceInputHandler",
    "MultipleChoiceInputHandler",
    "IndexedListInputHandler",
    "EnumChoiceInputHandler",
    # Security
    "PasswordInputHandler",
    "PinInputHandler",
    "ApiKeyInputHandler",
    "TokenInputHandler",
    "SecretTextInputHandler",
    # Composite/Structured
    "CredentialsInputHandler",
    "AddressInputHandler",
    "PhoneNumberInputHandler",
    "DateRangeInputHandler",
    "MultiFieldFormInputHandler",
]


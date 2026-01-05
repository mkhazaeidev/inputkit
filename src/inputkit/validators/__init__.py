"""
validators/__init__.py

Public API for all validation classes in inputkit.

This module provides a clean, flat interface to all validators organized by category:

Textual Inputs:
    - PlainTextValidator: Plain text with length constraints
    - UsernameValidator: Usernames and identifiers
    - FullNameValidator: Full names (multilingual)
    - EmailValidator: Email addresses
    - URLValidator: URLs (HTTP, HTTPS, FTP, file)
    - FilePathValidator: File paths (Unix/Windows)
    - CommandValidator: CLI command strings
    - MultiLineTextValidator: Multiline text input
    - SlugValidator: URL-friendly slugs

Numeric Inputs:
    - IntegerValidator: Integers (positive, negative, any)
    - FloatValidator: Floats (positive, negative, any)
    - RangeValidator: Range-limited numbers
    - PercentageValidator: Percentage values (0-100%)
    - YearValidator: Year values (1900-2099)
    - AgeValidator: Age values (0-150)

Boolean & Confirmation:
    - BooleanValidator: Yes/No, True/False, etc.
    - YesNoValidator: Yes/No only
    - TrueFalseValidator: True/False only
    - ContinueConfirmationValidator: Continue/proceed confirmations
    - AgreementValidator: Agreement/consent inputs

Security & Sensitive:
    - PasswordValidator: Password strength validation
    - PinValidator: PIN codes (4-12 digits)
    - ApiKeyValidator: API keys (32-128 chars)
    - TokenValidator: Tokens (JWT, hex, base64)
    - SecretTextValidator: Secret/hidden text

Structured/Composite:
    - CredentialsValidator: Username + password
    - AddressValidator: Country, city, postal code
    - PhoneNumberValidator: Phone numbers with country support
    - DateRangeValidator: Date ranges (start/end)
    - SingleChoiceValidator: Single choice from list
    - MultipleChoiceValidator: Multiple choices from list
    - IndexedListValidator: Selection by index
    - EnumValidator: Enum-based selection
    - MultiFieldFormValidator: Multi-field form validation

Common:
    - RequiredValidator: Required value check
    - OptionalValidator: Optional value wrapper

Core:
    - BaseValidator: Base class for all validators
    - CompositeValidator: Combine multiple validators

All validators support custom regex patterns and provide user-friendly error messages.

Purpose:
- Hide internal module structure from end-users.
- Make the validators package simple and intuitive to use.
- Provide a comprehensive validation toolkit for all input types.
"""

# Core validators
from .core import BaseValidator, CompositeValidator

# Textual validators
from .strings import (
    PlainTextValidator,
    UsernameValidator,
    FullNameValidator,
    EmailValidator,
    URLValidator,
    FilePathValidator,
    CommandValidator,
    MultiLineTextValidator,
    SlugValidator,
)

# Numeric validators
from .numeric import (
    IntegerValidator,
    FloatValidator,
    RangeValidator,
    PercentageValidator,
    YearValidator,
    AgeValidator,
)

# Boolean and confirmation validators
from .common import (
    RequiredValidator,
    OptionalValidator,
    BooleanValidator,
    YesNoValidator,
    TrueFalseValidator,
    ContinueConfirmationValidator,
    AgreementValidator,
)

# Security validators
from .security import (
    PasswordValidator,
    PinValidator,
    ApiKeyValidator,
    TokenValidator,
    SecretTextValidator,
)

# Composite/structured validators
from .composite import (
    CredentialsValidator,
    AddressValidator,
    PhoneNumberValidator,
    DateRangeValidator,
    SingleChoiceValidator,
    MultipleChoiceValidator,
    IndexedListValidator,
    EnumValidator,
    MultiFieldFormValidator,
)

__all__ = [
    # Core
    "BaseValidator",
    "CompositeValidator",
    # Textual
    "PlainTextValidator",
    "UsernameValidator",
    "FullNameValidator",
    "EmailValidator",
    "URLValidator",
    "FilePathValidator",
    "CommandValidator",
    "MultiLineTextValidator",
    "SlugValidator",
    # Numeric
    "IntegerValidator",
    "FloatValidator",
    "RangeValidator",
    "PercentageValidator",
    "YearValidator",
    "AgeValidator",
    # Boolean/Confirmation
    "RequiredValidator",
    "OptionalValidator",
    "BooleanValidator",
    "YesNoValidator",
    "TrueFalseValidator",
    "ContinueConfirmationValidator",
    "AgreementValidator",
    # Security
    "PasswordValidator",
    "PinValidator",
    "ApiKeyValidator",
    "TokenValidator",
    "SecretTextValidator",
    # Composite/Structured
    "CredentialsValidator",
    "AddressValidator",
    "PhoneNumberValidator",
    "DateRangeValidator",
    "SingleChoiceValidator",
    "MultipleChoiceValidator",
    "IndexedListValidator",
    "EnumValidator",
    "MultiFieldFormValidator",
]

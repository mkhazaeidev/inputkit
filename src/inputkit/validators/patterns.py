"""
patterns.py

Object-oriented pattern classes for regex-based input validation in inputkit.

Each class encapsulates a set of regular expressions and useful validation methods for a specific input category or data type. All patterns are thoroughly documented and designed for international use (e.g., E.164 for phone numbers, RFC specs for email/URL).

Categories:
    - UsernamePattern: Usernames, identifiers, slugs.
    - FullNamePattern: Personal names (multilingual support).
    - EmailPattern: RFC 5322-compliant emails.
    - URLPattern: Web and file URLs.
    - FilePathPattern: Unix/Windows file paths.
    - CommandPattern: Shell/CLI command strings.
    - MultiLineTextPattern: Detects multi-line text.
    - IntegerPattern, FloatPattern, PercentagePattern: Numeric string formats.
    - MobileNumberPattern: International phone numbers (with explicit Iran support).
    - BooleanPattern: Yes/No, True/False, confirmations.
    - PinPattern: PIN, API key, token and sensitive fields.
    - Additional patterns as necessary.

Patterns are intended for use in validators and composable input logic.
"""

import re
from typing import Pattern, Optional, Dict

class UsernamePattern:
    """
    Validation patterns for usernames, identifiers, and slugs.
    Supports strict (letters, digits, - and _) and relaxed (Unicode) modes.
    """
    STRICT: Pattern = re.compile(r"^[a-zA-Z0-9_-]{3,32}$")
    RELAXED: Pattern = re.compile(r"^[\w\-]{3,32}$", re.UNICODE)

    @classmethod
    def is_valid(cls, value: str, strict: bool = True) -> bool:
        """Check if value matches username pattern."""
        return bool(cls.STRICT.fullmatch(value) if strict else cls.RELAXED.fullmatch(value))

class FullNamePattern:
    """
    Validation for full names.
    Allows letters (Unicode basic Latin and common scripts), spaces, hyphens, and apostrophes (3-64 chars).
    Note: Not as broad as ICU/regex's \p{L}, but covers common use.
    """
    PATTERN: Pattern = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿĀ-ž\s.'-]{3,64}$")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class EmailPattern:
    """
    RFC 5322-compliant email validation (commonly used variant).
    """
    PATTERN: Pattern = re.compile(
        r"^(?i)[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
        r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,}$"
    )

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class URLPattern:
    """
    Patterns to match web URLs with HTTP(S)/FTP or file schemes.
    """
    PATTERN: Pattern = re.compile(
        r"^(?i)(https?|ftp|file)://[\w\-]+(\.[\w\-]+)+([:/?#\[\]@!$&'()*+,;=\w\-\.%]*)$"
    )

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class FilePathPattern:
    """
    Unix and Windows file path pattern.
    Accepts absolute or relative paths, with folders/files/extensions.
    """
    PATTERN: Pattern = re.compile(r"(^[a-zA-Z]:\\\\([\\w\\-. ]+\\\\)*[\\w\\-. ]+(\\.[\\w]+)?$|^(/[^/ ]*)+/?$)")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class CommandPattern:
    """
    Basic validation for CLI commands (no shell meta, no line break).
    """
    PATTERN: Pattern = re.compile(r"^[\w\d_ ./\\'\"|\-&:=%$#*@!]+$")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class MultiLineTextPattern:
    """
    Detects valid multi-line text input (2+ lines, any characters).
    """
    PATTERN: Pattern = re.compile(r"^(?:.*\n.*)+$")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.match(value))

class IntegerPattern:
    """
    Matches integer string (positive, negative, zero).
    """
    PATTERN: Pattern = re.compile(r"^[+-]?\d+$")
    POSITIVE: Pattern = re.compile(r"^\+?\d+$")
    NEGATIVE: Pattern = re.compile(r"^-\d+$")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))
    @classmethod
    def is_positive(cls, value: str) -> bool:
        return bool(cls.POSITIVE.fullmatch(value))
    @classmethod
    def is_negative(cls, value: str) -> bool:
        return bool(cls.NEGATIVE.fullmatch(value))

class FloatPattern:
    """
    Matches float string (with optional sign and decimals).
    """
    PATTERN: Pattern = re.compile(r"^[+-]?(\d+\.\d+|\d+\.|\.\d+)$")
    POSITIVE: Pattern = re.compile(r"^\+?(\d+\.\d+|\d+\.|\.\d+)$")
    NEGATIVE: Pattern = re.compile(r"^-((\d+\.\d+)|(\d+\.)|(\.\d+))$")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))
    @classmethod
    def is_positive(cls, value: str) -> bool:
        return bool(cls.POSITIVE.fullmatch(value))
    @classmethod
    def is_negative(cls, value: str) -> bool:
        return bool(cls.NEGATIVE.fullmatch(value))

class PercentagePattern:
    """
    Matches a percentage value string (0-100%, optional % sign).
    """
    PATTERN: Pattern = re.compile(r"^(100(\.0+)?|\d{1,2}(\.\d+)?)%?$")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class YearPattern:
    """
    Matches a four-digit year (>=1900, <= 2099).
    Use logic for stricter range if desired.
    """
    PATTERN: Pattern = re.compile(r"^(19\d{2}|20\d{2})$")
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class AgePattern:
    """
    Matches an age from 0-150 as string.
    """
    PATTERN: Pattern = re.compile(r"^(?:[1-9]?\d|1[01]\d|120|1[3-4][0-9]|150)$")
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class BooleanPattern:
    """
    Accepts yes/no, y/n, true/false, t/f, 0/1, on/off, etc. (Case insensitive).
    Used for CLI confirmation/boolean inputs.
    """
    PATTERN: Pattern = re.compile(
        r"^(?i)(y(es)?|no?|true|false|t|f|1|0|on|off|ok|sure|agree|confirm|cancel)$"
    )
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class PinPattern:
    """
    Accepts a PIN number (4-12 digits, can adjust as needed).
    """
    PATTERN: Pattern = re.compile(r"^\d{4,12}$")
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class ApiKeyPattern:
    """
    Accepts a generic API key (32-128 alphanumeric, may contain hyphens or underscores).
    """
    PATTERN: Pattern = re.compile(r"^[A-Za-z0-9_-]{32,128}$")
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class TokenPattern:
    """
    Accepts a generic token: JWT/Hex/Base64 (flexible, customizable per usage).
    """
    PATTERN: Pattern = re.compile(r"^[A-Za-z0-9\-_.=]+$")
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

class MobileNumberPattern:
    """
    Validates international mobile (cell) numbers using strict E.164, and supports country-specific detail.
    For Iran (country code +98), includes the most common prefixes (e.g. 09xx, +989xx).
    To add or override patterns for a country, update COUNTRY_PATTERNS.
    """
    E164: Pattern = re.compile(r"^\+\d{10,15}$")
    IR_09X: Pattern = re.compile(r"^(\+98|0)?9\d{9}$")
    COUNTRY_PATTERNS: Dict[str, Pattern] = {
        "IR": IR_09X,
        "US": re.compile(r"^(\+1)?[2-9]\d{2}[2-9](?!11)\d{6}$"),
        "UK": re.compile(r"^(\+44|0)7\d{9}$"),
        # Add more country regexes here as needed.
    }
    @classmethod
    def is_valid(cls, value: str, country: Optional[str] = None) -> bool:
        if country:
            pattern = cls.COUNTRY_PATTERNS.get(country.upper())
            if pattern:
                return bool(pattern.fullmatch(value))
        return bool(cls.E164.fullmatch(value))


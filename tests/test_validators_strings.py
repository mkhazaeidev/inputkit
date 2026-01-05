"""
Test suite for inputkit.validators.strings module.

Tests all textual input validators with valid and invalid cases.
"""
import pytest
import re
from inputkit.validators.strings import (
    PlainTextValidator, UsernameValidator, FullNameValidator, EmailValidator,
    URLValidator, FilePathValidator, CommandValidator, MultiLineTextValidator,
    SlugValidator
)
from inputkit.exceptions import ValidationError, LengthError, PatternMismatchError


class TestPlainTextValidator:
    def test_valid_text(self):
        validator = PlainTextValidator()
        assert validator.validate("Hello World") is True
    
    def test_min_length(self):
        validator = PlainTextValidator(min_length=5)
        assert validator.validate("Hello") is True
        with pytest.raises(LengthError):
            validator.validate("Hi")
    
    def test_max_length(self):
        validator = PlainTextValidator(max_length=10)
        assert validator.validate("Hello") is True
        with pytest.raises(LengthError):
            validator.validate("This is too long")
    
    def test_empty_text(self):
        validator = PlainTextValidator()
        with pytest.raises(ValidationError):
            validator.validate("")
    
    def test_custom_pattern(self):
        pattern = re.compile(r"^[A-Z]+$")
        validator = PlainTextValidator(custom_pattern=pattern)
        assert validator.validate("HELLO") is True
        with pytest.raises(PatternMismatchError):
            validator.validate("hello")


class TestUsernameValidator:
    def test_strict_valid(self):
        validator = UsernameValidator(strict=True)
        assert validator.validate("user_name-123") is True
    
    def test_strict_invalid(self):
        validator = UsernameValidator(strict=True)
        with pytest.raises(PatternMismatchError):
            validator.validate("user@name")
    
    def test_relaxed_valid(self):
        validator = UsernameValidator(strict=False)
        assert validator.validate("user_name-123") is True
    
    def test_custom_pattern(self):
        pattern = re.compile(r"^[a-z]{3,10}$")
        validator = UsernameValidator(custom_pattern=pattern)
        assert validator.validate("username") is True
        with pytest.raises(PatternMismatchError):
            validator.validate("USERNAME")


class TestFullNameValidator:
    def test_valid_name(self):
        validator = FullNameValidator()
        assert validator.validate("John Doe") is True
        assert validator.validate("Mary-Jane O'Neil") is True
    
    def test_invalid_name(self):
        validator = FullNameValidator()
        with pytest.raises(PatternMismatchError):
            validator.validate("123")
        with pytest.raises(PatternMismatchError):
            validator.validate("A")


class TestEmailValidator:
    def test_valid_email(self):
        validator = EmailValidator()
        assert validator.validate("test@example.com") is True
        assert validator.validate("user.name@domain.co.uk") is True
    
    def test_invalid_email(self):
        validator = EmailValidator()
        with pytest.raises(PatternMismatchError):
            validator.validate("invalid-email")
        with pytest.raises(PatternMismatchError):
            validator.validate("@domain.com")


class TestURLValidator:
    def test_valid_url(self):
        validator = URLValidator()
        assert validator.validate("https://example.com") is True
        assert validator.validate("ftp://host.name/file.txt") is True
    
    def test_invalid_url(self):
        validator = URLValidator()
        with pytest.raises(PatternMismatchError):
            validator.validate("not-a-url")


class TestFilePathValidator:
    def test_unix_path(self):
        validator = FilePathValidator()
        assert validator.validate("/usr/local/bin/file.sh") is True
    
    def test_windows_path(self):
        validator = FilePathValidator()
        assert validator.validate(r"C:\\Users\\file.txt") is True


class TestCommandValidator:
    def test_valid_command(self):
        validator = CommandValidator()
        assert validator.validate("ls -la /tmp") is True
    
    def test_invalid_command(self):
        validator = CommandValidator()
        # Commands with dangerous chars might fail
        with pytest.raises(PatternMismatchError):
            validator.validate("rm -rf /")


class TestMultiLineTextValidator:
    def test_valid_multiline(self):
        validator = MultiLineTextValidator()
        assert validator.validate("line1\nline2") is True
    
    def test_single_line(self):
        validator = MultiLineTextValidator()
        with pytest.raises(ValidationError):
            validator.validate("single line")


class TestSlugValidator:
    def test_valid_slug(self):
        validator = SlugValidator()
        assert validator.validate("my-slug-123") is True
    
    def test_invalid_slug(self):
        validator = SlugValidator()
        with pytest.raises(PatternMismatchError):
            validator.validate("My Slug")  # uppercase and space
        with pytest.raises(PatternMismatchError):
            validator.validate("slug_123")  # underscore


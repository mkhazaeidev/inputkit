"""
Test suite for inputkit.validators.security module.

Tests all security and sensitive input validators.
"""
import pytest
from inputkit.validators.security import (
    PasswordValidator, PinValidator, ApiKeyValidator,
    TokenValidator, SecretTextValidator
)
from inputkit.exceptions import PasswordStrengthError, ValidationError, LengthError


class TestPasswordValidator:
    def test_strong_password(self):
        validator = PasswordValidator()
        assert validator.validate("Password123!") is True
    
    def test_weak_password_too_short(self):
        validator = PasswordValidator(min_length=8)
        with pytest.raises(PasswordStrengthError):
            validator.validate("Pass1!")
    
    def test_weak_password_no_uppercase(self):
        validator = PasswordValidator()
        with pytest.raises(PasswordStrengthError):
            validator.validate("password123!")
    
    def test_weak_password_no_lowercase(self):
        validator = PasswordValidator()
        with pytest.raises(PasswordStrengthError):
            validator.validate("PASSWORD123!")
    
    def test_weak_password_no_digit(self):
        validator = PasswordValidator()
        with pytest.raises(PasswordStrengthError):
            validator.validate("Password!")
    
    def test_weak_password_no_special(self):
        validator = PasswordValidator()
        with pytest.raises(PasswordStrengthError):
            validator.validate("Password123")
    
    def test_custom_requirements(self):
        validator = PasswordValidator(
            min_length=12,
            require_uppercase=False,
            require_special=False
        )
        assert validator.validate("password1234") is True


class TestPinValidator:
    def test_valid_pin(self):
        validator = PinValidator()
        assert validator.validate("1234") is True
        assert validator.validate("123456789012") is True
    
    def test_pin_too_short(self):
        validator = PinValidator(min_length=4)
        with pytest.raises(ValidationError):
            validator.validate("123")
    
    def test_pin_too_long(self):
        validator = PinValidator(max_length=6)
        with pytest.raises(ValidationError):
            validator.validate("1234567")
    
    def test_invalid_pin_format(self):
        validator = PinValidator()
        with pytest.raises(ValidationError):
            validator.validate("abc")


class TestApiKeyValidator:
    def test_valid_api_key(self):
        validator = ApiKeyValidator()
        key = "a" * 32
        assert validator.validate(key) is True
    
    def test_api_key_too_short(self):
        validator = ApiKeyValidator(min_length=32)
        with pytest.raises(LengthError):
            validator.validate("short")
    
    def test_api_key_too_long(self):
        validator = ApiKeyValidator(max_length=64)
        key = "a" * 100
        with pytest.raises(LengthError):
            validator.validate(key)


class TestTokenValidator:
    def test_valid_token(self):
        validator = TokenValidator()
        assert validator.validate("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9") is True
        assert validator.validate("deadbeef1234==") is True
    
    def test_invalid_token(self):
        validator = TokenValidator()
        with pytest.raises(ValidationError):
            validator.validate("token with spaces")
        with pytest.raises(ValidationError):
            validator.validate("token!")


class TestSecretTextValidator:
    def test_valid_secret(self):
        validator = SecretTextValidator()
        assert validator.validate("secret123") is True
    
    def test_secret_too_short(self):
        validator = SecretTextValidator(min_length=10)
        with pytest.raises(LengthError):
            validator.validate("short")
    
    def test_secret_too_long(self):
        validator = SecretTextValidator(max_length=20)
        secret = "a" * 25
        with pytest.raises(LengthError):
            validator.validate(secret)


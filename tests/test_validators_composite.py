"""
Test suite for inputkit.validators.composite module.

Tests structured/composite and selection validators.
"""
import pytest
from enum import Enum
from inputkit.validators.composite import (
    CredentialsValidator, AddressValidator, PhoneNumberValidator,
    DateRangeValidator, SingleChoiceValidator, MultipleChoiceValidator,
    IndexedListValidator, EnumValidator, MultiFieldFormValidator
)
from inputkit.exceptions import ValidationError, RequiredValueError, MultiValidationError


class TestCredentialsValidator:
    def test_valid_credentials(self):
        validator = CredentialsValidator()
        assert validator.validate({"username": "user123", "password": "Password123!"}) is True
    
    def test_missing_username(self):
        validator = CredentialsValidator()
        with pytest.raises(RequiredValueError):
            validator.validate({"password": "Password123!"})
    
    def test_missing_password(self):
        validator = CredentialsValidator()
        with pytest.raises(RequiredValueError):
            validator.validate({"username": "user123"})


class TestAddressValidator:
    def test_valid_address(self):
        validator = AddressValidator()
        address = {
            "country": "United States",
            "city": "New York",
            "postal_code": "10001"
        }
        assert validator.validate(address) is True
    
    def test_missing_required_fields(self):
        validator = AddressValidator(require_country=True, require_city=True)
        with pytest.raises(RequiredValueError):
            validator.validate({"city": "New York"})
        with pytest.raises(RequiredValueError):
            validator.validate({"country": "USA"})


class TestPhoneNumberValidator:
    def test_valid_phone_iran(self):
        validator = PhoneNumberValidator(country="IR")
        assert validator.validate("09121234567") is True
        assert validator.validate("+989121234567") is True
    
    def test_valid_phone_us(self):
        validator = PhoneNumberValidator(country="US")
        assert validator.validate("+12025550123") is True
    
    def test_invalid_phone(self):
        validator = PhoneNumberValidator()
        with pytest.raises(ValidationError):
            validator.validate("invalid")


class TestDateRangeValidator:
    def test_valid_date_range(self):
        validator = DateRangeValidator()
        date_range = {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
        assert validator.validate(date_range) is True
    
    def test_invalid_date_range(self):
        validator = DateRangeValidator()
        with pytest.raises(ValidationError):
            validator.validate({
                "start_date": "2023-12-31",
                "end_date": "2023-01-01"
            })


class TestSingleChoiceValidator:
    def test_valid_choice(self):
        validator = SingleChoiceValidator(choices=["apple", "banana", "cherry"])
        assert validator.validate("apple") is True
    
    def test_invalid_choice(self):
        validator = SingleChoiceValidator(choices=["apple", "banana", "cherry"])
        with pytest.raises(ValidationError):
            validator.validate("orange")
    
    def test_case_insensitive(self):
        validator = SingleChoiceValidator(choices=["Apple", "Banana"], case_sensitive=False)
        assert validator.validate("apple") is True


class TestMultipleChoiceValidator:
    def test_valid_choices(self):
        validator = MultipleChoiceValidator(choices=["red", "green", "blue"])
        assert validator.validate(["red", "blue"]) is True
    
    def test_too_few_selections(self):
        validator = MultipleChoiceValidator(choices=["a", "b", "c"], min_selections=2)
        with pytest.raises(ValidationError):
            validator.validate(["a"])
    
    def test_too_many_selections(self):
        validator = MultipleChoiceValidator(choices=["a", "b", "c"], max_selections=2)
        with pytest.raises(ValidationError):
            validator.validate(["a", "b", "c"])


class TestIndexedListValidator:
    def test_valid_index(self):
        validator = IndexedListValidator(max_index=5)
        assert validator.validate(0) is True
        assert validator.validate(4) is True
    
    def test_invalid_index(self):
        validator = IndexedListValidator(max_index=5)
        with pytest.raises(ValidationError):
            validator.validate(5)
        with pytest.raises(ValidationError):
            validator.validate(-1)


class TestEnumValidator:
    def test_valid_enum(self):
        class Color(Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"
        
        validator = EnumValidator(Color)
        assert validator.validate(Color.RED) is True
        assert validator.validate("RED") is True
        assert validator.validate("red") is True
    
    def test_invalid_enum(self):
        class Color(Enum):
            RED = "red"
            GREEN = "green"
        
        validator = EnumValidator(Color)
        with pytest.raises(ValidationError):
            validator.validate("BLUE")


class TestMultiFieldFormValidator:
    def test_valid_form(self):
        from inputkit.validators.strings import UsernameValidator, EmailValidator
        from inputkit.validators.numeric import AgeValidator
        
        validators = {
            "username": UsernameValidator(),
            "email": EmailValidator(),
            "age": AgeValidator()
        }
        validator = MultiFieldFormValidator(field_validators=validators)
        
        form = {
            "username": "user123",
            "email": "user@example.com",
            "age": "25"
        }
        assert validator.validate(form) is True
    
    def test_invalid_form(self):
        from inputkit.validators.strings import UsernameValidator
        
        validators = {"username": UsernameValidator()}
        validator = MultiFieldFormValidator(field_validators=validators, require_all=True)
        
        with pytest.raises(MultiValidationError):
            validator.validate({"username": "invalid@username"})


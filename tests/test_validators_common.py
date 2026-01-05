"""
Test suite for inputkit.validators.common module.

Tests boolean, confirmation, and common validators.
"""
import pytest
from inputkit.validators.common import (
    RequiredValidator, OptionalValidator, BooleanValidator,
    YesNoValidator, TrueFalseValidator, ContinueConfirmationValidator,
    AgreementValidator
)
from inputkit.exceptions import RequiredValueError, ValidationError


class TestRequiredValidator:
    def test_valid_value(self):
        validator = RequiredValidator()
        assert validator.validate("value") is True
        assert validator.validate(123) is True
    
    def test_none_value(self):
        validator = RequiredValidator()
        with pytest.raises(RequiredValueError):
            validator.validate(None)
    
    def test_empty_string(self):
        validator = RequiredValidator()
        with pytest.raises(RequiredValueError):
            validator.validate("")
        with pytest.raises(RequiredValueError):
            validator.validate("   ")


class TestOptionalValidator:
    def test_none_value(self):
        validator = OptionalValidator()
        assert validator.validate(None) is True
        assert validator.validate("") is True
    
    def test_with_inner_validator(self):
        from inputkit.validators.strings import UsernameValidator
        inner = UsernameValidator()
        validator = OptionalValidator(inner_validator=inner)
        assert validator.validate(None) is True
        assert validator.validate("username123") is True
        with pytest.raises(ValidationError):
            validator.validate("invalid@username")


class TestBooleanValidator:
    def test_valid_boolean_strings(self):
        validator = BooleanValidator()
        assert validator.validate("yes") is True
        assert validator.validate("no") is True
        assert validator.validate("true") is True
        assert validator.validate("false") is True
        assert validator.validate("1") is True
        assert validator.validate("0") is True
    
    def test_python_bool(self):
        validator = BooleanValidator()
        assert validator.validate(True) is True
        assert validator.validate(False) is True
    
    def test_invalid_boolean(self):
        validator = BooleanValidator()
        with pytest.raises(ValidationError):
            validator.validate("maybe")


class TestYesNoValidator:
    def test_valid_yes_no(self):
        validator = YesNoValidator()
        assert validator.validate("yes") is True
        assert validator.validate("y") is True
        assert validator.validate("no") is True
        assert validator.validate("n") is True
    
    def test_invalid_yes_no(self):
        validator = YesNoValidator()
        with pytest.raises(ValidationError):
            validator.validate("true")
        with pytest.raises(ValidationError):
            validator.validate("1")


class TestTrueFalseValidator:
    def test_valid_true_false(self):
        validator = TrueFalseValidator()
        assert validator.validate("true") is True
        assert validator.validate("false") is True
        assert validator.validate("t") is True
        assert validator.validate("f") is True
        assert validator.validate(True) is True
        assert validator.validate(False) is True
    
    def test_invalid_true_false(self):
        validator = TrueFalseValidator()
        with pytest.raises(ValidationError):
            validator.validate("yes")


class TestContinueConfirmationValidator:
    def test_valid_confirmations(self):
        validator = ContinueConfirmationValidator()
        assert validator.validate("continue") is True
        assert validator.validate("proceed") is True
        assert validator.validate("yes") is True
        assert validator.validate("ok") is True
    
    def test_invalid_confirmation(self):
        validator = ContinueConfirmationValidator()
        with pytest.raises(ValidationError):
            validator.validate("cancel")


class TestAgreementValidator:
    def test_valid_agreements(self):
        validator = AgreementValidator()
        assert validator.validate("agree") is True
        assert validator.validate("accept") is True
        assert validator.validate("consent") is True
        assert validator.validate("yes") is True
    
    def test_invalid_agreement(self):
        validator = AgreementValidator()
        with pytest.raises(ValidationError):
            validator.validate("disagree")


"""
Test suite for inputkit.validators.numeric module.

Tests all numeric input validators with valid and invalid cases.
"""
import pytest
from inputkit.validators.numeric import (
    IntegerValidator, FloatValidator, RangeValidator, PercentageValidator,
    YearValidator, AgeValidator
)
from inputkit.exceptions import ValidationError, RangeError


class TestIntegerValidator:
    def test_valid_integer(self):
        validator = IntegerValidator()
        assert validator.validate("123") is True
        assert validator.validate(123) is True
    
    def test_positive_only(self):
        validator = IntegerValidator(positive_only=True)
        assert validator.validate("123") is True
        with pytest.raises(RangeError):
            validator.validate("-123")
    
    def test_negative_only(self):
        validator = IntegerValidator(negative_only=True)
        assert validator.validate("-123") is True
        with pytest.raises(RangeError):
            validator.validate("123")
    
    def test_invalid_integer(self):
        validator = IntegerValidator()
        with pytest.raises(ValidationError):
            validator.validate("12.5")
        with pytest.raises(ValidationError):
            validator.validate("abc")


class TestFloatValidator:
    def test_valid_float(self):
        validator = FloatValidator()
        assert validator.validate("3.14") is True
        assert validator.validate(3.14) is True
    
    def test_positive_only(self):
        validator = FloatValidator(positive_only=True)
        assert validator.validate("3.14") is True
        with pytest.raises(RangeError):
            validator.validate("-3.14")
    
    def test_invalid_float(self):
        validator = FloatValidator()
        with pytest.raises(ValidationError):
            validator.validate("abc")


class TestRangeValidator:
    def test_valid_range(self):
        validator = RangeValidator(min_value=1, max_value=100)
        assert validator.validate(50) is True
        assert validator.validate("50") is True
    
    def test_below_minimum(self):
        validator = RangeValidator(min_value=1, max_value=100)
        with pytest.raises(RangeError):
            validator.validate(0)
    
    def test_above_maximum(self):
        validator = RangeValidator(min_value=1, max_value=100)
        with pytest.raises(RangeError):
            validator.validate(101)
    
    def test_exclusive_bounds(self):
        validator = RangeValidator(min_value=1, max_value=100, min_inclusive=False, max_inclusive=False)
        assert validator.validate(50) is True
        with pytest.raises(RangeError):
            validator.validate(1)
        with pytest.raises(RangeError):
            validator.validate(100)


class TestPercentageValidator:
    def test_valid_percentage(self):
        validator = PercentageValidator()
        assert validator.validate("50") is True
        assert validator.validate("50%") is True
        assert validator.validate("100") is True
    
    def test_invalid_percentage(self):
        validator = PercentageValidator()
        with pytest.raises(ValidationError):
            validator.validate("150")
        with pytest.raises(ValidationError):
            validator.validate("abc")


class TestYearValidator:
    def test_valid_year(self):
        validator = YearValidator()
        assert validator.validate("2000") is True
        assert validator.validate(2000) is True
    
    def test_out_of_range(self):
        validator = YearValidator(min_year=2000, max_year=2020)
        with pytest.raises(RangeError):
            validator.validate("1999")
        with pytest.raises(RangeError):
            validator.validate("2021")


class TestAgeValidator:
    def test_valid_age(self):
        validator = AgeValidator()
        assert validator.validate("25") is True
        assert validator.validate(25) is True
    
    def test_out_of_range(self):
        validator = AgeValidator(min_age=18, max_age=65)
        with pytest.raises(RangeError):
            validator.validate("17")
        with pytest.raises(RangeError):
            validator.validate("66")


"""
Test suite for inputkit.input.numeric module.

Tests all numeric input handlers.
"""
import pytest
from unittest.mock import patch
from inputkit.input.numeric import (
    IntegerInputHandler, FloatInputHandler, RangeNumberInputHandler,
    PercentageInputHandler, YearInputHandler, AgeInputHandler
)
from inputkit.exceptions import ValidationError


class TestIntegerInputHandler:
    def test_get_integer(self):
        handler = IntegerInputHandler(prompt="Enter integer")
        with patch.object(handler.terminal, 'read_line', return_value='123'):
            result = handler.get()
            assert result == 123
    
    def test_get_positive_integer(self):
        handler = IntegerInputHandler(prompt="Enter integer", positive_only=True)
        with patch.object(handler.terminal, 'read_line', return_value='-5'):
            with pytest.raises(ValidationError):
                handler.get()
    
    def test_get_negative_integer(self):
        handler = IntegerInputHandler(prompt="Enter integer", negative_only=True)
        with patch.object(handler.terminal, 'read_line', return_value='-5'):
            result = handler.get()
            assert result == -5


class TestFloatInputHandler:
    def test_get_float(self):
        handler = FloatInputHandler(prompt="Enter number")
        with patch.object(handler.terminal, 'read_line', return_value='3.14'):
            result = handler.get()
            assert result == 3.14


class TestRangeNumberInputHandler:
    def test_get_in_range(self):
        handler = RangeNumberInputHandler(prompt="Enter number", min_value=1, max_value=100)
        with patch.object(handler.terminal, 'read_line', return_value='50'):
            result = handler.get()
            assert result == 50
    
    def test_get_out_of_range(self):
        handler = RangeNumberInputHandler(prompt="Enter number", min_value=1, max_value=100)
        with patch.object(handler.terminal, 'read_line', return_value='150'):
            with pytest.raises(ValidationError):
                handler.get()


class TestPercentageInputHandler:
    def test_get_percentage(self):
        handler = PercentageInputHandler(prompt="Enter percentage")
        with patch.object(handler.terminal, 'read_line', return_value='50'):
            result = handler.get()
            assert result == 50.0
    
    def test_get_percentage_with_sign(self):
        handler = PercentageInputHandler(prompt="Enter percentage")
        with patch.object(handler.terminal, 'read_line', return_value='75%'):
            result = handler.get()
            assert result == 75.0


class TestYearInputHandler:
    def test_get_year(self):
        handler = YearInputHandler(prompt="Enter year")
        with patch.object(handler.terminal, 'read_line', return_value='2023'):
            result = handler.get()
            assert result == 2023


class TestAgeInputHandler:
    def test_get_age(self):
        handler = AgeInputHandler(prompt="Enter age")
        with patch.object(handler.terminal, 'read_line', return_value='25'):
            result = handler.get()
            assert result == 25


"""
Test suite for inputkit.input.choices module.

Tests selection input handlers.
"""
import pytest
from enum import Enum
from unittest.mock import patch
from inputkit.input.choices import (
    SingleChoiceInputHandler, MultipleChoiceInputHandler,
    IndexedListInputHandler, EnumChoiceInputHandler
)


class TestSingleChoiceInputHandler:
    def test_get_by_index(self):
        handler = SingleChoiceInputHandler(choices=["apple", "banana", "cherry"], prompt="Select")
        with patch.object(handler.terminal, 'read_line', return_value='1'):
            with patch.object(handler.terminal, 'write'):
                result = handler.get()
                assert result == "apple"
    
    def test_get_by_value(self):
        handler = SingleChoiceInputHandler(choices=["apple", "banana", "cherry"], prompt="Select")
        with patch.object(handler.terminal, 'read_line', return_value='banana'):
            with patch.object(handler.terminal, 'write'):
                result = handler.get()
                assert result == "banana"


class TestMultipleChoiceInputHandler:
    def test_get_multiple(self):
        handler = MultipleChoiceInputHandler(choices=["red", "green", "blue"], prompt="Select")
        with patch.object(handler.terminal, 'read_line', return_value='red,blue'):
            with patch.object(handler.terminal, 'write'):
                result = handler.get()
                assert "red" in result
                assert "blue" in result


class TestIndexedListInputHandler:
    def test_get_by_index(self):
        handler = IndexedListInputHandler(items=["item1", "item2", "item3"], prompt="Select")
        with patch.object(handler.terminal, 'read_line', return_value='0'):
            with patch.object(handler.terminal, 'write'):
                result = handler.get()
                assert result == "item1"


class TestEnumChoiceInputHandler:
    def test_get_enum(self):
        class Color(Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"
        
        handler = EnumChoiceInputHandler(Color, prompt="Select color")
        with patch.object(handler.terminal, 'read_line', return_value='RED'):
            with patch.object(handler.terminal, 'write'):
                result = handler.get()
                assert result == Color.RED


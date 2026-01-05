"""
Test suite for inputkit.input.boolean module.

Tests boolean and confirmation input handlers.
"""
import pytest
from unittest.mock import patch
from inputkit.input.boolean import (
    YesNoInputHandler, TrueFalseInputHandler,
    ContinueConfirmationInputHandler, AgreementInputHandler
)


class TestYesNoInputHandler:
    def test_get_yes(self):
        handler = YesNoInputHandler(prompt="Continue?")
        with patch.object(handler.terminal, 'read_line', return_value='yes'):
            result = handler.get()
            assert result is True
    
    def test_get_no(self):
        handler = YesNoInputHandler(prompt="Continue?")
        with patch.object(handler.terminal, 'read_line', return_value='no'):
            result = handler.get()
            assert result is False


class TestTrueFalseInputHandler:
    def test_get_true(self):
        handler = TrueFalseInputHandler(prompt="Enter true/false")
        with patch.object(handler.terminal, 'read_line', return_value='true'):
            result = handler.get()
            assert result is True
    
    def test_get_false(self):
        handler = TrueFalseInputHandler(prompt="Enter true/false")
        with patch.object(handler.terminal, 'read_line', return_value='false'):
            result = handler.get()
            assert result is False


class TestContinueConfirmationInputHandler:
    def test_get_continue(self):
        handler = ContinueConfirmationInputHandler(prompt="Continue?")
        with patch.object(handler.terminal, 'read_line', return_value='continue'):
            result = handler.get()
            assert result is True


class TestAgreementInputHandler:
    def test_get_agree(self):
        handler = AgreementInputHandler(prompt="Do you agree?")
        with patch.object(handler.terminal, 'read_line', return_value='agree'):
            result = handler.get()
            assert result is True


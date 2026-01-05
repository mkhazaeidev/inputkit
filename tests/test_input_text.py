"""
Test suite for inputkit.input.text module.

Tests all textual input handlers.
"""
import pytest
from unittest.mock import Mock, patch
from inputkit.input.text import (
    PlainTextInputHandler, UsernameInputHandler, EmailInputHandler,
    URLInputHandler, MultiLineTextInputHandler
)
from inputkit.exceptions import ValidationError


class TestPlainTextInputHandler:
    def test_get_text(self):
        handler = PlainTextInputHandler(prompt="Enter text")
        with patch.object(handler.terminal, 'read_line', return_value='Hello'):
            result = handler.get()
            assert result == "Hello"
    
    def test_get_with_default(self):
        handler = PlainTextInputHandler(prompt="Enter text", default="default")
        with patch.object(handler.terminal, 'read_line', return_value=''):
            result = handler.get()
            assert result == "default"
    
    def test_get_with_min_length(self):
        handler = PlainTextInputHandler(prompt="Enter text", min_length=5)
        with patch.object(handler.terminal, 'read_line', return_value='Hi'):
            with pytest.raises(ValidationError):
                handler.get()


class TestUsernameInputHandler:
    def test_get_username(self):
        handler = UsernameInputHandler(prompt="Enter username")
        with patch.object(handler.terminal, 'read_line', return_value='user123'):
            result = handler.get()
            assert result == "user123"
    
    def test_get_invalid_username(self):
        handler = UsernameInputHandler(prompt="Enter username", strict=True)
        with patch.object(handler.terminal, 'read_line', return_value='user@name'):
            with pytest.raises(ValidationError):
                handler.get()


class TestEmailInputHandler:
    def test_get_email(self):
        handler = EmailInputHandler(prompt="Enter email")
        with patch.object(handler.terminal, 'read_line', return_value='test@example.com'):
            result = handler.get()
            assert result == "test@example.com"
    
    def test_get_invalid_email(self):
        handler = EmailInputHandler(prompt="Enter email")
        with patch.object(handler.terminal, 'read_line', return_value='invalid-email'):
            with pytest.raises(ValidationError):
                handler.get()


class TestURLInputHandler:
    def test_get_url(self):
        handler = URLInputHandler(prompt="Enter URL")
        with patch.object(handler.terminal, 'read_line', return_value='https://example.com'):
            result = handler.get()
            assert result == "https://example.com"


class TestMultiLineTextInputHandler:
    def test_get_multiline(self):
        handler = MultiLineTextInputHandler(prompt="Enter text")
        lines = ["line1", "line2", ""]
        with patch.object(handler.terminal, 'read_line', side_effect=lines):
            with patch.object(handler.terminal, 'write'):
                result = handler.get()
                assert "line1" in result
                assert "line2" in result


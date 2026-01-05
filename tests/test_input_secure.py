"""
Test suite for inputkit.input.secure module.

Tests secure input handlers.
"""
import pytest
from unittest.mock import patch
from inputkit.input.secure import (
    PasswordInputHandler, PinInputHandler, ApiKeyInputHandler
)
from inputkit.exceptions import ValidationError


class TestPasswordInputHandler:
    def test_get_password(self):
        handler = PasswordInputHandler(prompt="Enter password")
        with patch.object(handler.terminal, 'read_secure', return_value='Password123!'):
            result = handler.get()
            assert result == "Password123!"
    
    def test_get_weak_password(self):
        handler = PasswordInputHandler(prompt="Enter password", min_length=8)
        with patch.object(handler.terminal, 'read_secure', return_value='weak'):
            with pytest.raises(ValidationError):
                handler.get()


class TestPinInputHandler:
    def test_get_pin(self):
        handler = PinInputHandler(prompt="Enter PIN")
        with patch.object(handler.terminal, 'read_secure', return_value='1234'):
            result = handler.get()
            assert result == "1234"


class TestApiKeyInputHandler:
    def test_get_api_key(self):
        handler = ApiKeyInputHandler(prompt="Enter API key", min_length=32)
        key = "a" * 32
        with patch.object(handler.terminal, 'read_secure', return_value=key):
            result = handler.get()
            assert result == key


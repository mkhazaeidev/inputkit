"""
Test suite for inputkit.input.composite module.

Tests composite/structured input handlers.
"""
import pytest
from unittest.mock import patch
from inputkit.input.composite import (
    CredentialsInputHandler, AddressInputHandler,
    PhoneNumberInputHandler, DateRangeInputHandler
)


class TestCredentialsInputHandler:
    def test_get_credentials(self):
        handler = CredentialsInputHandler(prompt="Enter credentials")
        with patch.object(handler.terminal, 'read_line', return_value='user123'):
            with patch.object(handler.terminal, 'read_secure', return_value='Password123!'):
                with patch.object(handler.terminal, 'write'):
                    result = handler.get()
                    assert result["username"] == "user123"
                    assert result["password"] == "Password123!"


class TestAddressInputHandler:
    def test_get_address(self):
        handler = AddressInputHandler(prompt="Enter address")
        responses = ["United States", "New York", "10001"]
        with patch.object(handler.terminal, 'read_line', side_effect=responses):
            with patch.object(handler.terminal, 'write'):
                result = handler.get()
                assert "country" in result
                assert "city" in result


class TestPhoneNumberInputHandler:
    def test_get_phone_iran(self):
        handler = PhoneNumberInputHandler(prompt="Enter phone", country="IR")
        with patch.object(handler.terminal, 'read_line', return_value='09121234567'):
            result = handler.get()
            assert result == "09121234567"


class TestDateRangeInputHandler:
    def test_get_date_range(self):
        handler = DateRangeInputHandler(prompt="Enter date range")
        responses = ["2023-01-01", "2023-12-31"]
        with patch.object(handler.terminal, 'read_line', side_effect=responses):
            with patch.object(handler.terminal, 'write'):
                result = handler.get()
                assert "start_date" in result
                assert "end_date" in result


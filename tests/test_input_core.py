"""
Test suite for inputkit.input.core module.

Tests BaseInputHandler functionality including retry logic, defaults, validation, etc.
"""
import pytest
from unittest.mock import Mock, patch
from inputkit.input.core import BaseInputHandler
from inputkit.validators.core import BaseValidator
from inputkit.exceptions import ValidationError, EmptyInputError, RetryLimitExceeded


class ConcreteInputHandler(BaseInputHandler):
    """Concrete implementation for testing."""
    
    def _read_input(self) -> str:
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> str:
        return raw_input.strip()


class TestBaseInputHandler:
    def test_init(self):
        handler = ConcreteInputHandler(prompt="Test", default="default")
        assert handler.prompt == "Test"
        assert handler.default == "default"
    
    def test_format_prompt_with_default(self):
        handler = ConcreteInputHandler(prompt="Test", default="default")
        prompt = handler._format_prompt()
        assert "Test" in prompt
        assert "default" in prompt
    
    def test_format_prompt_with_help(self):
        handler = ConcreteInputHandler(prompt="Test", help_text="Help text")
        prompt = handler._format_prompt()
        assert "?" in prompt
    
    def test_format_prompt_with_hint(self):
        handler = ConcreteInputHandler(prompt="Test", hint="Hint text")
        prompt = handler._format_prompt()
        assert "Hint" in prompt
    
    def test_handle_help_request(self):
        handler = ConcreteInputHandler(prompt="Test", help_text="Help text")
        with patch.object(handler.terminal, 'write') as mock_write:
            result = handler._handle_help_request("?")
            assert result is True
            mock_write.assert_called_once()
    
    def test_process_input_with_default(self):
        handler = ConcreteInputHandler(prompt="Test", default="default", required=False)
        result = handler._process_input("")
        assert result == "default"
    
    def test_process_input_empty_required(self):
        handler = ConcreteInputHandler(prompt="Test", required=True)
        with pytest.raises(EmptyInputError):
            handler._process_input("")
    
    def test_process_input_with_validation(self):
        validator = Mock(spec=BaseValidator)
        validator.validate = Mock()
        handler = ConcreteInputHandler(prompt="Test", validator=validator)
        handler._process_input("test")
        validator.validate.assert_called_once_with("test")
    
    @patch('builtins.input', return_value='test')
    def test_get_success(self, mock_input):
        handler = ConcreteInputHandler(prompt="Test")
        with patch.object(handler.terminal, 'read_line', return_value='test'):
            handler.terminal.read_line = Mock(return_value='test')
            result = handler.get()
            assert result == "test"
    
    def test_get_with_default(self):
        handler = ConcreteInputHandler(prompt="Test", default="default", required=False)
        with patch.object(handler.terminal, 'read_line', return_value=''):
            result = handler.get()
            assert result == "default"
    
    def test_get_retry_on_validation_error(self):
        validator = Mock(spec=BaseValidator)
        validator.validate = Mock(side_effect=ValidationError("Invalid"))
        handler = ConcreteInputHandler(prompt="Test", validator=validator, retry_limit=2)
        with patch.object(handler.terminal, 'read_line', return_value='invalid'):
            with pytest.raises(RetryLimitExceeded):
                handler.get()


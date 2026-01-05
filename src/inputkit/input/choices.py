"""
choices.py

This module allows the user to select from a list of options.

Provides input handlers for:
- Single choice selection
- Multiple choice selection
- Indexed list selection
- Enum-based selection

All handlers support validators, retry logic, defaults, and help text.

Purpose:
- Provide flexible selection input in terminal applications.
- Make CLI interfaces interactive and user-friendly.
- Support various selection patterns.
"""

from typing import Optional, List, Any, Set
from enum import Enum

from .core import BaseInputHandler
from ..validators.core import BaseValidator
from ..validators.composite import (
    SingleChoiceValidator, MultipleChoiceValidator,
    IndexedListValidator, EnumValidator
)
from ..exceptions import InputCancelled


class SingleChoiceInputHandler(BaseInputHandler):
    """
    Handler for single choice selection from a list of options.
    
    Displays options as a numbered list and allows user to select by number or value.
    """
    
    def __init__(
        self,
        choices: List[Any],
        prompt: str = "Select an option",
        default: Optional[Any] = None,
        validator: Optional[BaseValidator] = None,
        case_sensitive: bool = True,
        display_format: str = "numbered",
        **kwargs
    ):
        """
        Initialize single choice input handler.
        
        Args:
            choices: List of available choices.
            prompt: Prompt text.
            default: Default value (must be in choices).
            validator: Optional custom validator.
            case_sensitive: If False, comparison is case-insensitive for strings.
            display_format: How to display choices ('numbered', 'bullet', 'plain').
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = SingleChoiceValidator(
                choices=choices,
                case_sensitive=case_sensitive,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.choices = choices
        self.case_sensitive = case_sensitive
        self.display_format = display_format
    
    def _display_choices(self) -> None:
        """Display choices to the user."""
        self.terminal.write(f"\n{self.prompt}:\n")
        for idx, choice in enumerate(self.choices, start=1):
            if self.display_format == "numbered":
                self.terminal.write(f"  {idx}. {choice}\n")
            elif self.display_format == "bullet":
                self.terminal.write(f"  • {choice}\n")
            else:
                self.terminal.write(f"  {choice}\n")
        self.terminal.write("\n")
    
    def _read_input(self) -> str:
        """Read single choice input."""
        self._display_choices()
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> Any:
        """Convert input to selected choice."""
        value = raw_input.strip()
        
        # Try to parse as index
        try:
            idx = int(value) - 1
            if 0 <= idx < len(self.choices):
                return self.choices[idx]
        except ValueError:
            pass
        
        # Try to match by value
        if self.case_sensitive:
            if value in self.choices:
                return value
        else:
            for choice in self.choices:
                if str(choice).lower() == value.lower():
                    return choice
        
        # If validator is set, it will catch invalid choices
        return value


class MultipleChoiceInputHandler(BaseInputHandler):
    """
    Handler for multiple choice selection from a list of options.
    
    Allows user to select multiple options (comma-separated or multiple prompts).
    """
    
    def __init__(
        self,
        choices: List[Any],
        prompt: str = "Select options",
        default: Optional[List[Any]] = None,
        validator: Optional[BaseValidator] = None,
        min_selections: int = 1,
        max_selections: Optional[int] = None,
        case_sensitive: bool = True,
        separator: str = ",",
        **kwargs
    ):
        """
        Initialize multiple choice input handler.
        
        Args:
            choices: List of available choices.
            prompt: Prompt text.
            default: Default value (list of choices).
            validator: Optional custom validator.
            min_selections: Minimum number of selections required.
            max_selections: Maximum number of selections allowed.
            case_sensitive: If False, comparison is case-insensitive for strings.
            separator: Separator for multiple selections (default: comma).
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = MultipleChoiceValidator(
                choices=choices,
                min_selections=min_selections,
                max_selections=max_selections,
                case_sensitive=case_sensitive,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.choices = choices
        self.min_selections = min_selections
        self.max_selections = max_selections
        self.case_sensitive = case_sensitive
        self.separator = separator
    
    def _display_choices(self) -> None:
        """Display choices to the user."""
        self.terminal.write(f"\n{self.prompt}:\n")
        for idx, choice in enumerate(self.choices, start=1):
            self.terminal.write(f"  {idx}. {choice}\n")
        self.terminal.write(f"(Select multiple options separated by '{self.separator}')\n\n")
    
    def _read_input(self) -> str:
        """Read multiple choice input."""
        self._display_choices()
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> List[Any]:
        """Convert input to list of selected choices."""
        values = [v.strip() for v in raw_input.split(self.separator)]
        result = []
        
        for value in values:
            # Try to parse as index
            try:
                idx = int(value) - 1
                if 0 <= idx < len(self.choices):
                    result.append(self.choices[idx])
                    continue
            except ValueError:
                pass
            
            # Try to match by value
            if self.case_sensitive:
                if value in self.choices:
                    result.append(value)
            else:
                for choice in self.choices:
                    if str(choice).lower() == value.lower():
                        result.append(choice)
                        break
        
        return result


class IndexedListInputHandler(BaseInputHandler):
    """
    Handler for indexed list selection (selection by index number).
    """
    
    def __init__(
        self,
        items: List[Any],
        prompt: str = "Select an item",
        default: Optional[int] = None,
        validator: Optional[BaseValidator] = None,
        **kwargs
    ):
        """
        Initialize indexed list input handler.
        
        Args:
            items: List of items to select from.
            prompt: Prompt text.
            default: Default index value.
            validator: Optional custom validator.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = IndexedListValidator(
                max_index=len(items),
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.items = items
    
    def _display_items(self) -> None:
        """Display items with indices."""
        self.terminal.write(f"\n{self.prompt}:\n")
        for idx, item in enumerate(self.items):
            self.terminal.write(f"  [{idx}] {item}\n")
        self.terminal.write("\n")
    
    def _read_input(self) -> str:
        """Read indexed selection input."""
        self._display_items()
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> Any:
        """Convert input to selected item."""
        idx = int(raw_input.strip())
        return self.items[idx]


class EnumChoiceInputHandler(BaseInputHandler):
    """
    Handler for enum-based selection.
    
    Allows user to select from enum values by name or value.
    """
    
    def __init__(
        self,
        enum_class: type,
        prompt: str = "Select an option",
        default: Optional[Enum] = None,
        validator: Optional[BaseValidator] = None,
        **kwargs
    ):
        """
        Initialize enum choice input handler.
        
        Args:
            enum_class: The enum class to select from.
            prompt: Prompt text.
            default: Default enum value.
            validator: Optional custom validator.
            **kwargs: Additional arguments passed to BaseInputHandler.
        """
        if validator is None:
            validator = EnumValidator(
                enum_class=enum_class,
                field_name=kwargs.get("field_name")
            )
        super().__init__(prompt=prompt, default=default, validator=validator, **kwargs)
        self.enum_class = enum_class
    
    def _display_enum_options(self) -> None:
        """Display enum options."""
        self.terminal.write(f"\n{self.prompt}:\n")
        for enum_member in self.enum_class:
            self.terminal.write(f"  {enum_member.name} = {enum_member.value}\n")
        self.terminal.write("\n")
    
    def _read_input(self) -> str:
        """Read enum selection input."""
        self._display_enum_options()
        return self.terminal.read_line()
    
    def _convert_value(self, raw_input: str) -> Enum:
        """Convert input to enum member."""
        value = raw_input.strip()
        
        # Try by name
        try:
            return self.enum_class[value]
        except KeyError:
            pass
        
        # Try by value
        try:
            return self.enum_class(value)
        except ValueError:
            pass
        
        # If validator is set, it will catch invalid enum values
        raise ValueError(f"Invalid enum value: {value}")

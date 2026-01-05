"""
terminal.py

Utilities for terminal input/output operations.

Provides TerminalManager class for handling terminal I/O operations across platforms.
Functions for clearing lines, formatting prompts, hiding input, and managing terminal state.
Handles low-level terminal behaviors across Windows, Linux, and macOS.

Purpose:
- Encapsulate terminal-specific logic.
- Provide smooth and consistent user experience in CLI.
- Abstract platform differences for terminal operations.
"""

import sys
import getpass
from typing import Optional

from .platform import PlatformDetector
from ..exceptions import TerminalNotAvailableError


class TerminalManager:
    """
    Manager for terminal input/output operations.
    
    Provides cross-platform terminal operations including:
    - Writing to stdout/stderr
    - Reading from stdin
    - Hiding input (for passwords)
    - Clearing lines
    - Managing terminal state
    """
    
    def __init__(self):
        """Initialize terminal manager."""
        self.platform = PlatformDetector()
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        self._stdin = sys.stdin
    
    def write(self, text: str, end: str = "") -> None:
        """
        Write text to stdout.
        
        Args:
            text: Text to write.
            end: End character (default: empty string).
        """
        try:
            self._stdout.write(text + end)
            self._stdout.flush()
        except (IOError, OSError) as e:
            raise TerminalNotAvailableError(feature="stdout", message=f"Cannot write to terminal: {e}")
    
    def write_error(self, text: str, end: str = "") -> None:
        """
        Write text to stderr.
        
        Args:
            text: Text to write.
            end: End character (default: empty string).
        """
        try:
            self._stderr.write(text + end)
            self._stderr.flush()
        except (IOError, OSError) as e:
            raise TerminalNotAvailableError(feature="stderr", message=f"Cannot write to terminal: {e}")
    
    def read_line(self) -> str:
        """
        Read a line from stdin.
        
        Returns:
            Input line (without trailing newline).
            
        Raises:
            TerminalNotAvailableError: If stdin is not available.
        """
        try:
            line = self._stdin.readline()
            if not line:
                raise EOFError("End of input")
            return line.rstrip('\n\r')
        except (IOError, OSError) as e:
            raise TerminalNotAvailableError(feature="stdin", message=f"Cannot read from terminal: {e}")
    
    def read_secure(self, prompt: str = "") -> str:
        """
        Read secure input (hidden, for passwords).
        
        Args:
            prompt: Optional prompt to display.
            
        Returns:
            Secure input string.
            
        Raises:
            TerminalNotAvailableError: If secure input is not available.
        """
        try:
            if prompt:
                self.write(prompt)
            return getpass.getpass("")
        except (IOError, OSError) as e:
            raise TerminalNotAvailableError(feature="secure_input", message=f"Cannot read secure input: {e}")
    
    def clear_line(self) -> None:
        """Clear the current line in terminal."""
        try:
            self.write("\r" + " " * 80 + "\r")
        except Exception:
            pass  # Ignore errors when clearing
    
    def is_interactive(self) -> bool:
        """
        Check if terminal is interactive.
        
        Returns:
            True if terminal is interactive, False otherwise.
        """
        return self._stdin.isatty() and self._stdout.isatty()

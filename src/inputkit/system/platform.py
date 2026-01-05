"""
platform.py

Platform detection utilities.

Provides PlatformDetector class for detecting OS type and platform-specific behaviors.
Detects Windows, Linux, macOS and provides helper functions for OS-specific operations.
Used internally by input and terminal modules.

Purpose:
- Ensure cross-platform compatibility for inputkit.
- Abstract away system-specific details.
- Provide platform-aware functionality.
"""

import platform
import sys
from typing import Optional

from ..exceptions import UnsupportedPlatformError


class PlatformDetector:
    """
    Detector for platform and OS information.
    
    Provides methods to detect:
    - Operating system type (Windows, Linux, macOS)
    - Platform-specific behaviors
    - Terminal capabilities
    """
    
    def __init__(self):
        """Initialize platform detector."""
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_linux = self.system == "linux"
        self.is_macos = self.system == "darwin"
        self.is_unix = self.is_linux or self.is_macos
    
    def get_platform(self) -> str:
        """
        Get platform name.
        
        Returns:
            Platform name: 'windows', 'linux', 'macos', or 'unknown'.
        """
        if self.is_windows:
            return "windows"
        elif self.is_linux:
            return "linux"
        elif self.is_macos:
            return "macos"
        else:
            return "unknown"
    
    def is_supported(self) -> bool:
        """
        Check if platform is supported.
        
        Returns:
            True if platform is supported, False otherwise.
        """
        return self.is_windows or self.is_linux or self.is_macos
    
    def check_support(self) -> None:
        """
        Check platform support and raise error if not supported.
        
        Raises:
            UnsupportedPlatformError: If platform is not supported.
        """
        if not self.is_supported():
            raise UnsupportedPlatformError(platform=self.get_platform())

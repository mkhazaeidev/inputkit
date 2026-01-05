"""
system.py

This module provides exceptions for system, platform, or terminal errors.

Classes:
    - SystemError: Base exception for inputkit system/platform failures.
    - UnsupportedPlatformError: Raised if the current OS is not supported.
    - TerminalNotAvailableError: For missing or unsupported terminal features.

These exceptions make system or environment issues explicit and easier to handle.
"""
from .base import InputKitError

class SystemError(InputKitError):
    """
    General exception for system/platform/terminal errors in inputkit.
    Args:
        message: Description of the system or platform error.
        **context: Diagnostic metadata.
    """
    def __init__(self, message=None, **context):
        if message is None:
            message = "A system or terminal error occurred."
        self.context = context
        super().__init__(message)

class UnsupportedPlatformError(SystemError):
    """
    Raised when the platform or OS does not support required features.
    Args:
        platform: A string identifying the unsupported platform.
    """
    def __init__(self, platform=None, message=None):
        if message is None:
            message = f"The platform {platform if platform else ''} is not supported by inputkit.".strip()
        super().__init__(message, platform=platform)

class TerminalNotAvailableError(SystemError):
    """
    Raised when required terminal features are unavailable for input/output.
    Args:
        feature: (Optional) Name of missing/unsupported terminal feature.
    """
    def __init__(self, feature=None, message=None):
        if message is None:
            if feature:
                message = f"Terminal feature '{feature}' is not available."
            else:
                message = "Required terminal is not available."
        super().__init__(message, feature=feature)


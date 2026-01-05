"""
base.py

Defines the base exception class for all inputkit errors.

Classes:
    - InputKitError: Base class for all project exceptions. Inherit from this for package-specific problems.

This design lets applications reliably catch all inputkit errors from one root.
"""

class InputKitError(Exception):
    """Base exception for all inputkit errors."""
    pass


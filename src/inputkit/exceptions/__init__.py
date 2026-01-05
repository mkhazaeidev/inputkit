"""
exceptions

The inputkit.exceptions package defines error classes for inputkit.

This package organizes exceptions by purpose:
    - base: Root exception class (InputKitError)
    - validation: For all validation/validator failures
    - input: For input workflow and user/cancellation errors
    - system: For platform or environment problems

Import exception classes for safe error handling in application code.
"""
from .validation import *
from .input import *
from .system import *

__all__ = []  # Expose public exception classes as needed

"""
core.py

This module contains the base classes and core logic for all input operations.

- BaseInput: the parent class for all input types.
- Handles retry logic, default values, and error management.
- Used internally by other input modules (text, secure, numeric, choices).

Purpose:
- Serve as the foundation for all user input functions.
- Keep common behaviors (like validation loops, prompts) in one place.
"""

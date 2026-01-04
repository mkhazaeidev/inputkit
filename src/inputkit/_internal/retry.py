"""
retry.py

Internal retry logic for input and validation.

- Handles re-prompting users on invalid input
- Works with BaseInput and validator functions
- Not exposed in the public API

Purpose:
- Provide a consistent retry mechanism for all input modules
- Keep loops and error handling internal
"""

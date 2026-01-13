"""
Custom exceptions for PyRate Framework.

All exceptions inherit from PyRateError for easy catching of framework-specific errors.
"""


class PyRateError(Exception):
    """Base class for all PyRate framework errors."""
    pass


class StepExecutionError(PyRateError):
    """
    Raised when a test step fails to execute.
    
    Attributes:
        step: The step that failed
        reason: Why it failed
    """
    def __init__(self, step: str, reason: str):
        self.step = step
        self.reason = reason
        super().__init__(f"❌ Error en paso: '{step}' | Causa: {reason}")


class ElementNotFoundError(PyRateError):
    """
    Raised when Playwright cannot find a UI element.
    
    Example:
        Raised when trying to click a button that doesn't exist in the DOM.
    """
    pass


class DataFileError(PyRateError):
    """
    Raised when data file loading fails.
    
    Examples:
        - File not found
        - Unsupported format
        - Malformed CSV/Excel/JSON
    """
    pass


class ApiConnectionError(PyRateError):
    """
    Raised when HTTP request fails.
    
    Examples:
        - Connection timeout
        - Network unreachable
        - Invalid URL
    """
    pass
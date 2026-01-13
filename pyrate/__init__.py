"""
PyRate Framework - Automation Testing for API and UI
=====================================================

A Python-based test automation framework inspired by Karate Framework,
combining API testing (requests) and UI testing (Playwright) with
Gherkin-style natural language syntax.

Key Features:
    - Natural language test syntax (Gherkin-style)
    - Dual testing: REST APIs + Browser UI
    - Data-driven testing (CSV, Excel, JSON)
    - Automatic evidence generation (DOCX, TXT)
    - Beautiful HTML reports
    - Fuzzy matchers for flexible assertions
    - Modular test execution with call read()

Example:
    >>> from pyrate import PyRateRunner
    >>> runner = PyRateRunner()
    >>> runner.execute_file("tests/features/login.feature")

Documentation:
    https://github.com/yourusername/pyrate
"""

__version__ = "1.0.1"
__author__ = "Your Name"
__license__ = "MIT"
__title__ = "PyRate Framework"
__description__ = "Automation testing framework for API and UI inspired by Karate"

from .core import PyRateRunner
from .assertions import Assertions
from .evidence import EvidenceGenerator
from .exceptions import (
    PyRateError,
    StepExecutionError,
    ElementNotFoundError,
    ApiConnectionError,
    DataFileError
)

__all__ = [
    # Core components
    "PyRateRunner",
    "Assertions",
    "EvidenceGenerator",
    
    # Exceptions
    "PyRateError",
    "StepExecutionError",
    "ElementNotFoundError",
    "ApiConnectionError",
    "DataFileError",
    
    # Metadata
    "__version__",
    "__author__",
    "__license__",
]

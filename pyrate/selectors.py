"""
Selector strategy module for PyRate Framework.

Supports CSS selectors and XPath expressions with automatic detection.
Compatible with Playwright locator API.

Examples:
    >>> from pyrate.selectors import SelectorStrategy, SelectorType
    >>> 
    >>> # CSS selector
    >>> selector_type, selector = SelectorStrategy.parse('#username')
    >>> print(selector_type, selector)
    SelectorType.CSS #username
    >>> 
    >>> # XPath with prefix
    >>> selector_type, selector = SelectorStrategy.parse('xpath=//input[@id="user"]')
    >>> print(selector_type, selector)
    SelectorType.XPATH //input[@id="user"]
    >>> 
    >>> # XPath auto-detect
    >>> selector_type, selector = SelectorStrategy.parse('//div[@class="login"]')
    >>> print(selector_type, selector)
    SelectorType.XPATH //div[@class="login"]
"""

from enum import Enum
from typing import Tuple


class SelectorType(Enum):
    """Types of selectors supported by PyRate."""
    CSS = "css"
    XPATH = "xpath"


class SelectorStrategy:
    """
    Parse and validate selectors for UI automation.
    
    Supports:
    - CSS selectors: '#username', '.btn-primary', 'input[type="text"]'
    - XPath with prefix: 'xpath=//input[@id="user"]'
    - XPath auto-detect: '//input[@id="user"]', '/html/body/div'
    
    The parser automatically detects the selector type:
    1. If starts with 'xpath=' → XPath (prefix removed)
    2. If starts with '//' or '/' → XPath (auto-detected)
    3. Otherwise → CSS (default)
    """
    
    @staticmethod
    def parse(selector: str) -> Tuple[SelectorType, str]:
        """
        Parse selector string and return (type, cleaned_selector).
        
        Args:
            selector: Raw selector string from Gherkin step
            
        Returns:
            Tuple of (SelectorType, cleaned_selector)
            
        Examples:
            >>> SelectorStrategy.parse('#username')
            (SelectorType.CSS, '#username')
            
            >>> SelectorStrategy.parse('xpath=//input')
            (SelectorType.XPATH, '//input')
            
            >>> SelectorStrategy.parse('//div[@class="test"]')
            (SelectorType.XPATH, '//div[@class="test"]')
            
            >>> SelectorStrategy.parse('.btn-primary')
            (SelectorType.CSS, '.btn-primary')
        """
        if not selector:
            raise ValueError("Selector cannot be empty")
        
        # Explicit XPath prefix
        if selector.startswith('xpath='):
            cleaned = selector[6:]  # Remove 'xpath=' prefix
            return (SelectorType.XPATH, cleaned)
        
        # Auto-detect XPath (starts with // or /)
        if selector.startswith('//') or selector.startswith('/'):
            return (SelectorType.XPATH, selector)
        
        # Default to CSS
        return (SelectorType.CSS, selector)
    
    @staticmethod
    def validate(selector_type: SelectorType, selector: str) -> bool:
        """
        Validate selector syntax (basic validation).
        
        Args:
            selector_type: SelectorType.CSS or SelectorType.XPATH
            selector: Selector string to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If selector is invalid
            
        Examples:
            >>> SelectorStrategy.validate(SelectorType.CSS, '#username')
            True
            
            >>> SelectorStrategy.validate(SelectorType.XPATH, '//input')
            True
            
            >>> SelectorStrategy.validate(SelectorType.XPATH, 'invalid')
            Traceback (most recent call last):
                ...
            ValueError: Invalid XPath: must start with / or //
        """
        if not selector:
            raise ValueError("Selector cannot be empty")
        
        if selector_type == SelectorType.XPATH:
            # Basic XPath validation: must start with / or //
            if not (selector.startswith('//') or selector.startswith('/')):
                raise ValueError(
                    f"Invalid XPath: must start with / or //. Got: {selector}"
                )
        
        if selector_type == SelectorType.CSS:
            # Basic CSS validation: not empty
            if not selector or selector.isspace():
                raise ValueError("Empty CSS selector")
        
        return True
    
    @staticmethod
    def format_for_playwright(selector_type: SelectorType, selector: str) -> str:
        """
        Format selector for Playwright locator API.
        
        Args:
            selector_type: Type of selector
            selector: Selector string
            
        Returns:
            Formatted selector string for Playwright
            
        Examples:
            >>> SelectorStrategy.format_for_playwright(SelectorType.CSS, '#user')
            '#user'
            
            >>> SelectorStrategy.format_for_playwright(SelectorType.XPATH, '//input')
            'xpath=//input'
        """
        if selector_type == SelectorType.XPATH:
            return f"xpath={selector}"
        return selector

"""
Validation utilities for PyRate Framework.

Provides reusable validation functions for URLs, JSON, selectors, and other inputs.
"""

import re
import json
from urllib.parse import urlparse
from typing import Optional


def is_valid_url(url: str) -> bool:
    """
    Check if a string is a valid URL.
    
    Args:
        url: String to validate as URL
        
    Returns:
        True if valid URL, False otherwise
        
    Examples:
        >>> is_valid_url("https://example.com")
        True
        >>> is_valid_url("not a url")
        False
        >>> is_valid_url("http://api.example.com/users")
        True
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_valid_json(text: str) -> bool:
    """
    Check if a string is valid JSON.
    
    Args:
        text: String to validate as JSON
        
    Returns:
        True if valid JSON, False otherwise
        
    Examples:
        >>> is_valid_json('{"key": "value"}')
        True
        >>> is_valid_json('[1, 2, 3]')
        True
        >>> is_valid_json('not json')
        False
    """
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def is_valid_selector(selector: str) -> bool:
    """
    Validate if a string looks like a valid CSS selector.
    
    This is a basic check, not comprehensive validation.
    
    Args:
        selector: CSS selector string
        
    Returns:
        True if it looks like a valid selector, False otherwise
        
    Examples:
        >>> is_valid_selector("#username")
        True
        >>> is_valid_selector(".btn-primary")
        True
        >>> is_valid_selector("button[type='submit']")
        True
        >>> is_valid_selector("")
        False
    """
    if not selector or not isinstance(selector, str):
        return False
    
    # Very basic check - not empty and contains valid CSS selector characters
    # More comprehensive validation would require a CSS parser
    valid_pattern = r'^[a-zA-Z0-9\s\.\#\[\]\=\'\"\-\_\:\>\+\~\*\,\(\)]+$'
    return bool(re.match(valid_pattern, selector.strip()))


def is_valid_http_method(method: str) -> bool:
    """
    Check if a string is a valid HTTP method.
    
    Args:
        method: HTTP method to validate
        
    Returns:
        True if valid HTTP method, False otherwise
        
    Examples:
        >>> is_valid_http_method("GET")
        True
        >>> is_valid_http_method("post")
        True
        >>> is_valid_http_method("INVALID")
        False
    """
    valid_methods = {
        'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 
        'HEAD', 'OPTIONS', 'TRACE', 'CONNECT'
    }
    return method.upper() in valid_methods


def is_valid_status_code(code: int) -> bool:
    """
    Check if an integer is a valid HTTP status code.
    
    Args:
        code: HTTP status code to validate
        
    Returns:
        True if valid status code (100-599), False otherwise
        
    Examples:
        >>> is_valid_status_code(200)
        True
        >>> is_valid_status_code(404)
        True
        >>> is_valid_status_code(999)
        False
    """
    return isinstance(code, int) and 100 <= code <= 599


def sanitize_filename(text: str, max_length: int = 100) -> str:
    """
    Convert text to a safe filename by removing/replacing invalid characters.
    
    Args:
        text: Text to convert to filename
        max_length: Maximum length for filename
        
    Returns:
        Sanitized filename string
        
    Examples:
        >>> sanitize_filename("Test: Login Flow")
        'Test_Login_Flow'
        >>> sanitize_filename("User@Email.com")
        'User_Email_com'
    """
    # Replace invalid filename characters with underscore
    safe_chars = re.sub(r'[<>:"/\\|?*\s]', '_', text)
    # Remove consecutive underscores
    safe_chars = re.sub(r'_+', '_', safe_chars)
    # Trim to max length
    return safe_chars[:max_length].strip('_')

"""
Configuration management for PyRate Framework.

This module provides the configuration system for PyRate, supporting both
programmatic configuration and YAML-based configuration files.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import os


@dataclass
class PyRateConfig:
    """
    Central configuration class for PyRate Framework.
    
    All configuration options are defined here with sensible defaults.
    Can be overridden via YAML configuration file or programmatically.
    
    Attributes:
        evidence_folder: Directory for test evidence files (default: "evidence")
        screenshot_on_pass: Take screenshots on passing UI steps (default: True)
        screenshot_on_fail: Take screenshots on failing steps (default: True)
        reports_folder: Directory for HTML reports (default: "reports")
        headless: Run browser in headless mode (default: False)
        browser_timeout: Browser operation timeout in milliseconds (default: 30000)
        api_timeout: API request timeout in seconds (default: 30)
        verify_ssl: Verify SSL certificates for API requests (default: True)
        retry_attempts: Number of retry attempts for failed API requests (default: 1)
        retry_delay: Delay between retries in seconds (default: 1.0)
        default_user_agent: Default User-Agent header for requests
        default_headers: Default HTTP headers for API requests
        max_response_log_size: Maximum size of response data in logs (default: 500)
    
    Example:
        >>> config = PyRateConfig(headless=True, api_timeout=60)
        >>> config.evidence_folder
        'evidence'
    """
    
    # Evidence settings
    evidence_folder: str = "evidence"
    screenshot_on_pass: bool = True
    screenshot_on_fail: bool = True
    
    # Report settings
    reports_folder: str = "reports"
    
    # Browser settings
    headless: bool = False
    browser_timeout: int = 30000  # milliseconds
    
    # API settings
    api_timeout: int = 30  # seconds
    verify_ssl: bool = True
    retry_attempts: int = 1
    retry_delay: float = 1.0
    
    # HTTP headers
    default_user_agent: str = "PyRate/1.0 (Automation Framework)"
    default_headers: Dict[str, str] = field(default_factory=lambda: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    
    # Logging
    max_response_log_size: int = 500
    verbose: bool = False
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'PyRateConfig':
        """
        Create PyRateConfig from a dictionary.
        
        Args:
            config_dict: Dictionary with configuration values
            
        Returns:
            PyRateConfig instance
            
        Example:
            >>> config_dict = {"headless": True, "api_timeout": 60}
            >>> config = PyRateConfig.from_dict(config_dict)
        """
        # Filter out keys that aren't valid config attributes
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}
        return cls(**filtered_dict)
    
    def to_dict(self) -> Dict:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of config
        """
        return {
            "evidence_folder": self.evidence_folder,
            "screenshot_on_pass": self.screenshot_on_pass,
            "screenshot_on_fail": self.screenshot_on_fail,
            "reports_folder": self.reports_folder,
            "headless": self.headless,
            "browser_timeout": self.browser_timeout,
            "api_timeout": self.api_timeout,
            "verify_ssl": self.verify_ssl,
            "retry_attempts": self.retry_attempts,
            "retry_delay": self.retry_delay,
            "default_user_agent": self.default_user_agent,
            "max_response_log_size": self.max_response_log_size,
            "verbose": self.verbose,
        }
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.browser_timeout < 0:
            raise ValueError("browser_timeout must be positive")
        if self.api_timeout <= 0:
            raise ValueError("api_timeout must be positive")
        if self.retry_attempts < 1:
            raise ValueError("retry_attempts must be at least 1")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
        
        # Create output folders if they don't exist
        os.makedirs(self.evidence_folder, exist_ok=True)
        os.makedirs(self.reports_folder, exist_ok=True)

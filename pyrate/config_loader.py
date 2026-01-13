"""
Configuration loader for PyRate Framework.

Handles loading configuration from YAML files with fallback to defaults.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

from .config import PyRateConfig


class ConfigLoader:
    """
    Loads PyRate configuration from YAML files or environment variables.
    
    Search order:
    1. Explicit config file path (if provided)
    2. pyrate.config.yaml in current directory
    3. Default configuration values
    
    Example:
        >>> config = ConfigLoader.load()
        >>> config = ConfigLoader.load("custom_config.yaml")
    """
    
    DEFAULT_CONFIG_NAMES = [
        "pyrate.config.yaml",
        "pyrate.config.yml",
        ".pyrate.yaml",
        ".pyrate.yml"
    ]
    
    @staticmethod
    def load(config_path: Optional[str] = None) -> PyRateConfig:
        """
        Load configuration from YAML file or use defaults.
        
        Args:
            config_path: Optional path to YAML configuration file
            
        Returns:
            PyRateConfig instance with loaded configuration
            
        Raises:
            FileNotFoundError: If specified config_path doesn't exist
            yaml.YAMLError: If YAML file is malformed
            
        Example:
            >>> config = ConfigLoader.load()
            >>> config = ConfigLoader.load("my_config.yaml")
        """
        config_dict = {}
        
        # 1. Try explicit path if provided
        if config_path:
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            config_dict = ConfigLoader._load_yaml_file(config_path)
        else:
            # 2. Try default config files in current directory
            for filename in ConfigLoader.DEFAULT_CONFIG_NAMES:
                if os.path.exists(filename):
                    config_dict = ConfigLoader._load_yaml_file(filename)
                    break
        
        # 3. Extract 'pyrate' section if it exists (nested config)
        if 'pyrate' in config_dict:
            config_dict = ConfigLoader._flatten_config(config_dict['pyrate'])
        
        # 4. Create PyRateConfig from dict (or use all defaults if empty)
        return PyRateConfig.from_dict(config_dict) if config_dict else PyRateConfig()
    
    @staticmethod
    def _load_yaml_file(file_path: str) -> Dict[str, Any]:
        """
        Load and parse YAML file.
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            Parsed YAML as dictionary
            
        Raises:
            yaml.YAMLError: If YAML is malformed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data if data else {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")
    
    @staticmethod
    def _flatten_config(config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten nested configuration dictionary to match PyRateConfig attributes.
        
        Supports both flat and nested YAML structures:
        
        Flat:
            evidence_folder: "evidence"
            headless: true
            
        Nested:
            evidence:
                folder: "evidence"
            browser:
                headless: true
        
        Args:
            config_dict: Nested configuration dictionary
            
        Returns:
            Flattened configuration dictionary
        """
        flattened = {}
        
        # Map nested keys to flat PyRateConfig attributes
        mappings = {
            ('evidence', 'folder'): 'evidence_folder',
            ('evidence', 'screenshot_on_pass'): 'screenshot_on_pass',
            ('evidence', 'screenshot_on_fail'): 'screenshot_on_fail',
            ('reports', 'folder'): 'reports_folder',
            ('browser', 'headless'): 'headless',
            ('browser', 'timeout'): 'browser_timeout',
            ('api', 'timeout'): 'api_timeout',
            ('api', 'verify_ssl'): 'verify_ssl',
            ('api', 'retry_attempts'): 'retry_attempts',
            ('api', 'retry_delay'): 'retry_delay',
            ('api', 'user_agent'): 'default_user_agent',
            ('logging', 'verbose'): 'verbose',
            ('logging', 'max_response_size'): 'max_response_log_size',
        }
        
        # Process nested structure
        for (parent_key, child_key), target_key in mappings.items():
            if parent_key in config_dict and isinstance(config_dict[parent_key], dict):
                if child_key in config_dict[parent_key]:
                    flattened[target_key] = config_dict[parent_key][child_key]
        
        # Also support flat keys directly (for backwards compatibility)
        for key, value in config_dict.items():
            if not isinstance(value, dict):  # Only flat values
                flattened[key] = value
        
        return flattened
    
    @staticmethod
    def save_example_config(output_path: str = "pyrate.config.yaml.example") -> None:
        """
        Generate an example configuration file with all options documented.
        
        Args:
            output_path: Path where to save the example file
            
        Example:
            >>> ConfigLoader.save_example_config()
        """
        example_yaml = """# PyRate Framework Configuration Example
# ==========================================
# Copy this file to 'pyrate.config.yaml' and customize as needed

pyrate:
  # Evidence generation settings
  evidence:
    folder: "evidence"              # Where to store evidence files
    screenshot_on_pass: true        # Capture screenshots on successful UI steps
    screenshot_on_fail: true        # Capture screenshots on failed steps
  
  # Report generation settings
  reports:
    folder: "reports"               # Where to store HTML reports
  
  # Browser automation settings (Playwright)
  browser:
    headless: false                 # Run browser in headless mode (true for CI)
    timeout: 30000                  # Timeout for browser operations (milliseconds)
  
  # API testing settings
  api:
    timeout: 30                     # Timeout for HTTP requests (seconds)
    verify_ssl: true                # Verify SSL certificates
    retry_attempts: 3               # Number of retry attempts for failed requests
    retry_delay: 1.0                # Delay between retries (seconds)
    user_agent: "PyRate/1.0"        # Custom User-Agent header
  
  # Logging settings
  logging:
    verbose: false                  # Enable verbose logging
    max_response_size: 500          # Maximum response data to log (characters)
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(example_yaml)
        
        print(f"✅ Example configuration saved to: {output_path}")

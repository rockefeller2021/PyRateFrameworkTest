"""
Tests for PyRate configuration loader.
"""
import pytest
import os
import tempfile
from pyrate.config import PyRateConfig
from pyrate.config_loader import ConfigLoader
class TestConfigDefaults:
    """Test default configuration values."""
    
    def test_default_config_values(self):
        """Should have sensible default values."""
        config = PyRateConfig()
        
        assert config.evidence_folder == "evidence"
        assert config.reports_folder == "reports"
        assert config.headless is False
        assert config.browser_timeout == 30000
        assert config.api_timeout == 30
        assert config.verify_ssl is True
        assert config.retry_attempts == 1
    
    def test_default_headers_exist(self):
        """Should have default HTTP headers."""
        config = PyRateConfig()
        
        assert "Content-Type" in config.default_headers
        assert "Accept" in config.default_headers
    
    def test_config_validation_browser_timeout(self):
        """Should validate browser timeout is positive."""
        with pytest.raises(ValueError, match="browser_timeout must be positive"):
            PyRateConfig(browser_timeout=-1)
    
    def test_config_validation_api_timeout(self):
        """Should validate API timeout is positive."""
        with pytest.raises(ValueError, match="api_timeout must be positive"):
            PyRateConfig(api_timeout=0)
    
    def test_config_validation_retry_attempts(self):
        """Should validate retry attempts is at least 1."""
        with pytest.raises(ValueError, match="retry_attempts must be at least 1"):
            PyRateConfig(retry_attempts=0)
class TestConfigFromDict:
    """Test creating config from dictionary."""
    
    def test_from_dict_basic(self):
        """Should create config from flat dictionary."""
        config_dict = {
            "headless": True,
            "api_timeout": 60,
            "retry_attempts": 5
        }
        
        config = PyRateConfig.from_dict(config_dict)
        
        assert config.headless is True
        assert config.api_timeout == 60
        assert config.retry_attempts == 5
    
    def test_from_dict_filters_invalid_keys(self):
        """Should ignore keys not in PyRateConfig."""
        config_dict = {
            "headless": True,
            "invalid_key": "should be ignored"
        }
        
        config = PyRateConfig.from_dict(config_dict)
        assert config.headless is True
class TestConfigLoader:
    """Test YAML configuration loading."""
    
    def test_load_without_file_returns_defaults(self):
        """Should return default config when no file exists."""
        config = ConfigLoader.load()
        
        assert config.evidence_folder == "evidence"
        assert config.headless is False
    
    def test_load_from_yaml_file(self):
        """Should load configuration from YAML file."""
        yaml_content = """
pyrate:
  browser:
    headless: true
    timeout: 60000
  api:
    timeout: 60
    retry_attempts: 5
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            config = ConfigLoader.load(temp_path)
            
            assert config.headless is True
            assert config.browser_timeout == 60000
            assert config.api_timeout == 60
            assert config.retry_attempts == 5
        finally:
            os.unlink(temp_path)
    
    def test_load_nonexistent_file_raises_error(self):
        """Should raise FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            ConfigLoader.load("nonexistent_config.yaml")
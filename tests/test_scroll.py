"""
Integration tests for Sprint 3 - Scroll Commands

Tests all scroll functionality:
- Scroll to element
- Scroll to top
- Scroll to bottom
- Scroll to coordinates
"""

import pytest
from pyrate.core import PyRateRunner
from pyrate.config import PyRateConfig


class TestScrollCommands:
    """Test suite for scroll commands"""
    
    def test_scroll_to_element(self, tmp_path):
        """Test scrolling to a specific element"""
        feature_file = tmp_path / "scroll_element.feature"
        feature_file.write_text("""
Scenario: Scroll to element
    Given driver 'https://the-internet.herokuapp.com/large'
    And scroll to element '#content'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Scroll to element should succeed"
    
    def test_scroll_to_top(self, tmp_path):
        """Test scrolling to top of page"""
        feature_file = tmp_path / "scroll_top.feature"
        feature_file.write_text("""
Scenario: Scroll to top
    Given driver 'https://the-internet.herokuapp.com/large'
    And scroll to bottom
    And wait 1
    And scroll to top
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Scroll to top should succeed"
    
    def test_scroll_to_bottom(self, tmp_path):
        """Test scrolling to bottom of page"""
        feature_file = tmp_path / "scroll_bottom.feature"
        feature_file.write_text("""
Scenario: Scroll to bottom
    Given driver 'https://the-internet.herokuapp.com/large'
    And scroll to bottom
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Scroll to bottom should succeed"
    
    def test_scroll_to_coordinates(self, tmp_path):
        """Test scrolling to specific coordinates"""
        feature_file = tmp_path / "scroll_coords.feature"
        feature_file.write_text("""
Scenario: Scroll to coordinates
    Given driver 'https://the-internet.herokuapp.com/large'
    And scroll to 0, 500
    And wait 1
    And scroll to 0, 1000
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Scroll to coordinates should succeed"
    
    def test_scroll_with_xpath(self, tmp_path):
        """Test scrolling to element using XPath"""
        feature_file = tmp_path / "scroll_xpath.feature"
        feature_file.write_text("""
Scenario: Scroll to element with XPath
    Given driver 'https://the-internet.herokuapp.com/large'
    And scroll to element '//div[@id="content"]'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Scroll with XPath should succeed"

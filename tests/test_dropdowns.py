"""
Integration tests for Sprint 3 - Dropdown/Select Commands

Tests all dropdown selection methods:
- Select by text
- Select by value
- Select by index
"""

import pytest
from pyrate.core import PyRateRunner
from pyrate.config import PyRateConfig


class TestDropdownCommands:
    """Test suite for dropdown/select commands"""
    
    def test_select_by_text(self, tmp_path):
        """Test selecting dropdown option by visible text"""
        feature_file = tmp_path / "select_text.feature"
        feature_file.write_text("""
Scenario: Select dropdown by text
    Given driver 'https://the-internet.herokuapp.com/dropdown'
    And select '#dropdown' by text 'Option 1'
    And wait 1
    And select '#dropdown' by text 'Option 2'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Select by text should succeed"
    
    def test_select_by_value(self, tmp_path):
        """Test selecting dropdown option by value attribute"""
        feature_file = tmp_path / "select_value.feature"
        feature_file.write_text("""
Scenario: Select dropdown by value
    Given driver 'https://the-internet.herokuapp.com/dropdown'
    And select '#dropdown' by value '1'
    And wait 1
    And select '#dropdown' by value '2'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Select by value should succeed"
    
    def test_select_by_index(self, tmp_path):
        """Test selecting dropdown option by index"""
        feature_file = tmp_path / "select_index.feature"
        feature_file.write_text("""
Scenario: Select dropdown by index
    Given driver 'https://the-internet.herokuapp.com/dropdown'
    And select '#dropdown' by index 1
    And wait 1
    And select '#dropdown' by index 2
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Select by index should succeed"
    
    def test_select_with_xpath(self, tmp_path):
        """Test selecting dropdown using XPath"""
        feature_file = tmp_path / "select_xpath.feature"
        feature_file.write_text("""
Scenario: Select dropdown with XPath
    Given driver 'https://the-internet.herokuapp.com/dropdown'
    And select '//select[@id="dropdown"]' by text 'Option 1'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Select with XPath should succeed"

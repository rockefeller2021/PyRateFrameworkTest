"""
Integration tests for Sprint 3 - Checkbox Commands

Tests all checkbox operations:
- Check checkbox
- Uncheck checkbox
- Toggle checkbox
"""

import pytest
from pyrate.core import PyRateRunner
from pyrate.config import PyRateConfig


class TestCheckboxCommands:
    """Test suite for checkbox commands"""
    
    def test_check_checkbox(self, tmp_path):
        """Test checking a checkbox"""
        feature_file = tmp_path / "check_checkbox.feature"
        feature_file.write_text("""
Scenario: Check checkbox
    Given driver 'https://the-internet.herokuapp.com/checkboxes'
    And check '//input[@type="checkbox"][1]'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Check checkbox should succeed"
    
    def test_uncheck_checkbox(self, tmp_path):
        """Test unchecking a checkbox"""
        feature_file = tmp_path / "uncheck_checkbox.feature"
        feature_file.write_text("""
Scenario: Uncheck checkbox
    Given driver 'https://the-internet.herokuapp.com/checkboxes'
    And uncheck '//input[@type="checkbox"][2]'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Uncheck checkbox should succeed"
    
    def test_toggle_checkbox(self, tmp_path):
        """Test toggling checkbox state"""
        feature_file = tmp_path / "toggle_checkbox.feature"
        feature_file.write_text("""
Scenario: Toggle checkbox
    Given driver 'https://the-internet.herokuapp.com/checkboxes'
    And toggle '//input[@type="checkbox"][1]'
    And wait 1
    And toggle '//input[@type="checkbox"][1]'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Toggle checkbox should succeed"
    
    def test_multiple_checkboxes(self, tmp_path):
        """Test handling multiple checkboxes"""
        feature_file = tmp_path / "multiple_checkboxes.feature"
        feature_file.write_text("""
Scenario: Handle multiple checkboxes
    Given driver 'https://the-internet.herokuapp.com/checkboxes'
    And check '//input[@type="checkbox"][1]'
    And check '//input[@type="checkbox"][2]'
    And wait 1
    And uncheck '//input[@type="checkbox"][1]'
    And uncheck '//input[@type="checkbox"][2]'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Multiple checkboxes should succeed"

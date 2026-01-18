"""
Integration tests for Sprint 3 - Radio Button Commands

Tests radio button selection
"""

import pytest
from pyrate.core import PyRateRunner
from pyrate.config import PyRateConfig


class TestRadioCommands:
    """Test suite for radio button commands"""
    
    def test_check_radio_button(self, tmp_path):
        """Test selecting a radio button"""
        feature_file = tmp_path / "radio_check.feature"
        feature_file.write_text("""
Scenario: Check radio button
    Given driver 'https://www.selenium.dev/selenium/web/web-form.html'
    And check radio '//input[@id="my-radio-1"]'
    And wait 1
    And check radio '//input[@id="my-radio-2"]'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Check radio button should succeed"
    
    def test_radio_button_group(self, tmp_path):
        """Test selecting from radio button group"""
        feature_file = tmp_path / "radio_group.feature"
        feature_file.write_text("""
Scenario: Select from radio group
    Given driver 'https://www.selenium.dev/selenium/web/web-form.html'
    And check radio '//input[@value="1"]'
    And wait 1
    And check radio '//input[@value="2"]'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Radio group selection should succeed"
    
    def test_radio_with_css_selector(self, tmp_path):
        """Test radio button with CSS selector"""
        feature_file = tmp_path / "radio_css.feature"
        feature_file.write_text("""
Scenario: Radio with CSS selector
    Given driver 'https://www.selenium.dev/selenium/web/web-form.html'
    And check radio '#my-radio-1'
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Radio with CSS should succeed"

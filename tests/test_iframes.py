"""
Integration tests for Sprint 3 - Iframe Commands

Tests iframe navigation:
- Switch to frame by selector
- Switch to frame by index
- Switch to default content
- Switch to parent frame
"""

import pytest
from pyrate.core import PyRateRunner
from pyrate.config import PyRateConfig


class TestIframeCommands:
    """Test suite for iframe commands"""
    
    def test_switch_to_frame_by_selector(self, tmp_path):
        """Test switching to iframe by CSS selector"""
        feature_file = tmp_path / "iframe_selector.feature"
        feature_file.write_text("""
Scenario: Switch to iframe by selector
    Given driver 'https://the-internet.herokuapp.com/iframe'
    And switch to frame '#mce_0_ifr'
    And wait 1
    And switch to default content
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Switch to frame by selector should succeed"
    
    def test_switch_to_default_content(self, tmp_path):
        """Test switching back to main page"""
        feature_file = tmp_path / "iframe_default.feature"
        feature_file.write_text("""
Scenario: Switch to default content
    Given driver 'https://the-internet.herokuapp.com/iframe'
    And switch to frame '#mce_0_ifr'
    And wait 1
    And switch to default content
    And wait 1
    And switch to main
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Switch to default should succeed"
    
    def test_switch_to_parent_frame(self, tmp_path):
        """Test switching to parent frame"""
        feature_file = tmp_path / "iframe_parent.feature"
        feature_file.write_text("""
Scenario: Switch to parent frame
    Given driver 'https://the-internet.herokuapp.com/iframe'
    And switch to frame '#mce_0_ifr'
    And wait 1
    And switch to parent
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Switch to parent should succeed"
    
    def test_nested_iframes(self, tmp_path):
        """Test navigating nested iframes"""
        feature_file = tmp_path / "iframe_nested.feature"
        feature_file.write_text("""
Scenario: Navigate nested iframes
    Given driver 'https://the-internet.herokuapp.com/nested_frames'
    And switch to frame '//frame[@name="frame-top"]'
    And wait 1
    And switch to default content
    And wait 1
""")
        
        config = PyRateConfig(headless=True)
        runner = PyRateRunner(config=config)
        runner.execute_file(str(feature_file))
        
        assert runner.is_success, "Nested iframes should succeed"

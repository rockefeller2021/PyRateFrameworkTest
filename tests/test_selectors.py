"""
Unit tests for selector strategy module.

Tests CSS and XPath selector parsing, validation, and Playwright formatting.
"""

import pytest
from pyrate.selectors import SelectorStrategy, SelectorType


class TestSelectorParsing:
    """Test selector type detection and parsing."""
    
    def test_css_selector_default(self):
        """CSS selectors should be detected as default."""
        selector_type, selector = SelectorStrategy.parse('#username')
        assert selector_type == SelectorType.CSS
        assert selector == '#username'
    
    def test_css_selector_class(self):
        """CSS class selectors should work."""
        selector_type, selector = SelectorStrategy.parse('.btn-primary')
        assert selector_type == SelectorType.CSS
        assert selector == '.btn-primary'
    
    def test_css_selector_attribute(self):
        """CSS attribute selectors should work."""
        selector_type, selector = SelectorStrategy.parse('input[type="text"]')
        assert selector_type == SelectorType.CSS
        assert selector == 'input[type="text"]'
    
    def test_xpath_with_prefix(self):
        """XPath with explicit xpath= prefix should be detected."""
        selector_type, selector = SelectorStrategy.parse('xpath=//input[@id="user"]')
        assert selector_type == SelectorType.XPATH
        assert selector == '//input[@id="user"]'
    
    def test_xpath_auto_detect_double_slash(self):
        """XPath starting with // should be auto-detected."""
        selector_type, selector = SelectorStrategy.parse('//div[@class="login"]')
        assert selector_type == SelectorType.XPATH
        assert selector == '//div[@class="login"]'
    
    def test_xpath_auto_detect_single_slash(self):
        """XPath starting with / should be auto-detected."""
        selector_type, selector = SelectorStrategy.parse('/html/body/div')
        assert selector_type == SelectorType.XPATH
        assert selector == '/html/body/div'
    
    def test_xpath_complex_expression(self):
        """Complex XPath expressions should work."""
        selector_type, selector = SelectorStrategy.parse(
            '//button[contains(@class, "submit") and text()="Login"]'
        )
        assert selector_type == SelectorType.XPATH
        assert selector == '//button[contains(@class, "submit") and text()="Login"]'
    
    def test_empty_selector_raises_error(self):
        """Empty selector should raise ValueError."""
        with pytest.raises(ValueError, match="Selector cannot be empty"):
            SelectorStrategy.parse('')


class TestSelectorValidation:
    """Test selector validation logic."""
    
    def test_validate_css_success(self):
        """Valid CSS selector should pass validation."""
        assert SelectorStrategy.validate(SelectorType.CSS, '#username') is True
    
    def test_validate_xpath_success(self):
        """Valid XPath should pass validation."""
        assert SelectorStrategy.validate(SelectorType.XPATH, '//input') is True
    
    def test_validate_xpath_invalid_raises_error(self):
        """XPath not starting with / should fail."""
        with pytest.raises(ValueError, match="Invalid XPath"):
            SelectorStrategy.validate(SelectorType.XPATH, 'invalid-xpath')
    
    def test_validate_empty_css_raises_error(self):
        """Empty CSS selector should fail."""
        with pytest.raises(ValueError, match="Empty CSS selector"):
            SelectorStrategy.validate(SelectorType.CSS, '')
    
    def test_validate_whitespace_css_raises_error(self):
        """Whitespace-only CSS selector should fail."""
        with pytest.raises(ValueError, match="Empty CSS selector"):
            SelectorStrategy.validate(SelectorType.CSS, '   ')


class TestPlaywrightFormatting:
    """Test Playwright locator formatting."""
    
    def test_format_css_selector(self):
        """CSS selector should remain unchanged."""
        formatted = SelectorStrategy.format_for_playwright(
            SelectorType.CSS, 
            '#username'
        )
        assert formatted == '#username'
    
    def test_format_xpath_selector(self):
        """XPath selector should be prefixed with xpath=."""
        formatted = SelectorStrategy.format_for_playwright(
            SelectorType.XPATH,
            '//input[@id="user"]'
        )
        assert formatted == 'xpath=//input[@id="user"]'


class TestBackwardCompatibility:
    """Test that existing CSS selectors still work (backward compatibility)."""
    
    def test_backward_compatible_id(self):
        """Existing #id selectors should work unchanged."""
        selector_type, selector = SelectorStrategy.parse('#user-name')
        assert selector_type == SelectorType.CSS
        assert selector == '#user-name'
    
    def test_backward_compatible_class(self):
        """Existing .class selectors should work unchanged."""
        selector_type, selector = SelectorStrategy.parse('.btn-submit')
        assert selector_type == SelectorType.CSS
        assert selector == '.btn-submit'
    
    def test_backward_compatible_tag(self):
        """Existing tag selectors should work unchanged."""
        selector_type, selector = SelectorStrategy.parse('button')
        assert selector_type == SelectorType.CSS
        assert selector == 'button'


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_xpath_with_spaces(self):
        """XPath with spaces should be preserved."""
        selector_type, selector = SelectorStrategy.parse(
            '//div[contains(text(), "Hello World")]'
        )
        assert selector == '//div[contains(text(), "Hello World")]'
    
    def test_css_with_multiple_selectors(self):
        """CSS with multiple selectors should work."""
        selector_type, selector = SelectorStrategy.parse('input.form-control#username')
        assert selector_type == SelectorType.CSS
        assert selector == 'input.form-control#username'
    
    def test_xpath_prefix_removal(self):
        """xpath= prefix should be removed cleanly."""
        _, selector = SelectorStrategy.parse('xpath=//div')
        assert not selector.startswith('xpath=')
        assert selector == '//div'

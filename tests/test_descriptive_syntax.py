"""
Unit tests for descriptive Gherkin syntax feature.

Tests comment-based descriptions before commands for better evidence generation.
"""

import unittest
from unittest.mock import Mock, patch
from pyrate.core import PyRateRunner


class TestDescriptiveSyntax(unittest.TestCase):
    """Test descriptive comment syntax in Gherkin steps."""
    
    def setUp(self):
        """Set up test runner."""
        self.runner = PyRateRunner()
        # Mock the context to avoid actual execution
        self.runner.context = {
            'page': None,
            'response': None,
            'response_json': {},
            'vars': {},
            'headers': {},
            'base_url': '',
            'auth': None,
            'verify_ssl': True,
            'cert': None,
            'request_body': None,
            'last_method': 'UNKNOWN'
        }
    
    def test_description_captured_and_used(self):
        """Description comment should be captured and used as step name."""
        lines = [
            "# Navigate to login page",
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # Verify description was used as step name
        self.assertEqual(len(scenario_log), 1)
        self.assertEqual(scenario_log[0]['name'], "Navigate to login page")
        self.assertEqual(scenario_log[0]['raw_command'], "Given url 'https://example.com'")
        self.assertEqual(scenario_log[0]['status'], "PASS")
    
    def test_no_description_uses_command(self):
        """Without description, step name should be the command itself."""
        lines = [
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # Name should be the command when no description
        self.assertEqual(len(scenario_log), 1)
        self.assertEqual(scenario_log[0]['name'], "Given url 'https://example.com'")
        self.assertEqual(scenario_log[0]['raw_command'], "Given url 'https://example.com'")
    
    def test_multiple_consecutive_descriptions(self):
        """Multiple consecutive descriptions should use only the last one."""
        lines = [
            "# First description",
            "# Second description",
            "# Third description (should be used)",
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # Only last description should be used
        self.assertEqual(len(scenario_log), 1)
        self.assertEqual(scenario_log[0]['name'], "Third description (should be used)")
    
    def test_tag_not_captured_as_description(self):
        """Tags like '# @smoke' should not be captured as descriptions."""
        lines = [
            "# @smoke",
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # Tag should not be used as description
        self.assertEqual(len(scenario_log), 1)
        self.assertEqual(scenario_log[0]['name'], "Given url 'https://example.com'")
    
    def test_tag_with_multiple_tags_not_captured(self):
        """Multiple tags like '# @smoke @ui' should not be captured."""
        lines = [
            "# @smoke @ui @regression",
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        self.assertEqual(scenario_log[0]['name'], "Given url 'https://example.com'")
    
    def test_description_reset_after_use(self):
        """Description should be reset after being used."""
        lines = [
            "# First step description",
            "Given url 'https://example.com'",
            "And path 'users/1'"  # No description for this step
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # First step should have description
        self.assertEqual(scenario_log[0]['name'], "First step description")
        
        # Second step should use command (no description)
        self.assertEqual(scenario_log[1]['name'], "And path 'users/1'")
    
    def test_mixed_descriptions_and_no_descriptions(self):
        """Test mix of steps with and without descriptions."""
        lines = [
            "# Set base URL",
            "Given url 'https://api.example.com'",
            "And path 'users'",  # No description
            "# Execute GET request",
            "When method get"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        self.assertEqual(len(scenario_log), 3)
        self.assertEqual(scenario_log[0]['name'], "Set base URL")
        self.assertEqual(scenario_log[1]['name'], "And path 'users'")
        self.assertEqual(scenario_log[2]['name'], "Execute GET request")
    
    def test_empty_comment_not_used_as_description(self):
        """Empty comment '#' should not be used as description."""
        lines = [
            "#",
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # Empty description should result in command being used
        self.assertEqual(scenario_log[0]['name'], "Given url 'https://example.com'")
    
    def test_whitespace_only_comment_not_used(self):
        """Comment with only whitespace should not be used."""
        lines = [
            "#    ",
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # Whitespace-only becomes empty string after strip, command is used
        # But our implementation captures line[1:].strip() which would be empty
        # So name should be empty string or command? Let's verify behavior
        # Actually, empty string would be falsy, so command is used
        self.assertEqual(scenario_log[0]['name'], "Given url 'https://example.com'")
    
    def test_description_with_special_characters(self):
        """Description can contain special characters."""
        lines = [
            "# Navigate to URL: https://example.com/login?redirect=/dashboard",
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        self.assertEqual(
            scenario_log[0]['name'],
            "Navigate to URL: https://example.com/login?redirect=/dashboard"
        )
    
    def test_description_with_quotes(self):
        """Description can contain quotes."""
        lines = [
            '# Input username "admin" in field',
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        self.assertEqual(scenario_log[0]['name'], 'Input username "admin" in field')


class TestBackwardCompatibility(unittest.TestCase):
    """Ensure backward compatibility with existing features."""
    
    def setUp(self):
        """Set up test runner."""
        self.runner = PyRateRunner()
        self.runner.context = {
            'page': None,
            'response': None,
            'response_json': {},
            'vars': {},
            'headers': {},
            'base_url': '',
            'auth': None,
            'verify_ssl': True,
            'cert': None,
            'request_body': None,
            'last_method': 'UNKNOWN'
        }
    
    def test_existing_tests_without_descriptions_work(self):
        """Existing test files without descriptions should work unchanged."""
        lines = [
            "Given url 'https://jsonplaceholder.typicode.com'",
            "And path 'users/1'",
            "When method get"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # All steps should execute normally
        self.assertEqual(len(scenario_log), 3)
        for step in scenario_log:
            self.assertEqual(step['status'], "PASS")
    
    def test_tags_still_filtered(self):
        """Tags like @smoke should still be filtered out."""
        lines = [
            "@smoke",
            "@ui",
            "Given url 'https://example.com'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        # Only the command should be in log, tags filtered
        self.assertEqual(len(scenario_log), 1)
    
    def test_empty_lines_still_skipped(self):
        """Empty lines should still be skipped."""
        lines = [
            "",
            "Given url 'https://example.com'",
            "",
            "And path 'users'"
        ]
        
        scenario_log = self.runner._execute_lines(lines)
        
        self.assertEqual(len(scenario_log), 2)


if __name__ == '__main__':
    unittest.main()

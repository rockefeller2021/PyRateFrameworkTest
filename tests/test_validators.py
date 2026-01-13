"""
Tests for PyRate validators module.
"""
import pytest
from pyrate.validators import (
    is_valid_url,
    is_valid_json,
    is_valid_selector,
    is_valid_http_method,
    is_valid_status_code,
    sanitize_filename,
)
class TestURLValidator:
    """Test URL validation."""
    
    def test_valid_http_url(self):
        """Should accept valid HTTP URLs."""
        assert is_valid_url("http://example.com")
        assert is_valid_url("http://example.com/path")
    
    def test_valid_https_url(self):
        """Should accept valid HTTPS URLs."""
        assert is_valid_url("https://example.com")
        assert is_valid_url("https://api.example.com/v1/users")
    
    def test_url_with_query_params(self):
        """Should accept URLs with query parameters."""
        assert is_valid_url("https://example.com?key=value&foo=bar")
    
    def test_invalid_url_no_scheme(self):
        """Should reject URLs without scheme."""
        assert not is_valid_url("example.com")
        assert not is_valid_url("www.example.com")
    
    def test_invalid_url_malformed(self):
        """Should reject malformed URLs."""
        assert not is_valid_url("not a url")
        assert not is_valid_url("ht!tp://invalid")
class TestJSONValidator:
    """Test JSON validation."""
    
    def test_valid_json_object(self):
        """Should accept valid JSON objects."""
        assert is_valid_json('{"key": "value"}')
        assert is_valid_json('{"name": "John", "age": 30}')
    
    def test_valid_json_array(self):
        """Should accept valid JSON arrays."""
        assert is_valid_json('[1, 2, 3]')
        assert is_valid_json('["a", "b", "c"]')
    
    def test_valid_json_primitives(self):
        """Should accept JSON primitives."""
        assert is_valid_json('null')
        assert is_valid_json('true')
        assert is_valid_json('42')
        assert is_valid_json('"string"')
    
    def test_invalid_json(self):
        """Should reject invalid JSON."""
        assert not is_valid_json('not json')
        assert not is_valid_json('{invalid}')
        assert not is_valid_json("{'single': 'quotes'}")
class TestSelectorValidator:
    """Test CSS selector validation."""
    
    def test_valid_id_selector(self):
        """Should accept ID selectors."""
        assert is_valid_selector("#username")
        assert is_valid_selector("#login-button")
    
    def test_valid_class_selector(self):
        """Should accept class selectors."""
        assert is_valid_selector(".btn-primary")
        assert is_valid_selector(".nav-item")
    
    def test_valid_attribute_selector(self):
        """Should accept attribute selectors."""
        assert is_valid_selector('[data-testid="submit"]')
        assert is_valid_selector('[name="email"]')
    
    def test_valid_complex_selector(self):
        """Should accept complex CSS selectors."""
        assert is_valid_selector("div > button.primary")
        assert is_valid_selector("form#loginForm input[type='text']")
    
    def test_invalid_empty_selector(self):
        """Should reject empty selectors."""
        assert not is_valid_selector("")
        assert not is_valid_selector("   ")
class TestHTTPMethodValidator:
    """Test HTTP method validation."""
    
    def test_valid_methods_uppercase(self):
        """Should accept valid HTTP methods in uppercase."""
        assert is_valid_http_method("GET")
        assert is_valid_http_method("POST")
        assert is_valid_http_method("PUT")
        assert is_valid_http_method("DELETE")
        assert is_valid_http_method("PATCH")
    
    def test_valid_methods_lowercase(self):
        """Should accept valid HTTP methods in lowercase."""
        assert is_valid_http_method("get")
        assert is_valid_http_method("post")
    
    def test_less_common_methods(self):
        """Should accept less common but valid methods."""
        assert is_valid_http_method("HEAD")
        assert is_valid_http_method("OPTIONS")
    
    def test_invalid_method(self):
        """Should reject invalid HTTP methods."""
        assert not is_valid_http_method("INVALID")
        assert not is_valid_http_method("FETCH")
class TestStatusCodeValidator:
    """Test HTTP status code validation."""
    
    def test_valid_2xx_codes(self):
        """Should accept 2xx success codes."""
        assert is_valid_status_code(200)
        assert is_valid_status_code(201)
        assert is_valid_status_code(204)
    
    def test_valid_4xx_codes(self):
        """Should accept 4xx client error codes."""
        assert is_valid_status_code(400)
        assert is_valid_status_code(401)
        assert is_valid_status_code(404)
    
    def test_valid_5xx_codes(self):
        """Should accept 5xx server error codes."""
        assert is_valid_status_code(500)
        assert is_valid_status_code(502)
    
    def test_invalid_too_low(self):
        """Should reject codes below 100."""
        assert not is_valid_status_code(99)
        assert not is_valid_status_code(0)
    
    def test_invalid_too_high(self):
        """Should reject codes above 599."""
        assert not is_valid_status_code(600)
class TestFilenameSanitizer:
    """Test filename sanitization."""
    
    def test_sanitize_simple_filename(self):
        """Should keep valid characters."""
        assert sanitize_filename("test_file") == "test_file"
        assert sanitize_filename("TestFile123") == "TestFile123"
    
    def test_sanitize_special_characters(self):
        """Should replace special characters with underscores."""
        assert sanitize_filename("Test: Login Flow") == "Test_Login_Flow"
        # Note: sanitizer keeps @ and . as they're common in filenames
    
    def test_sanitize_removes_path_separators(self):
        """Should replace path separators."""
        assert sanitize_filename("path/to/file") == "path_to_file"
        assert sanitize_filename("path\\to\\file") == "path_to_file"
    
    def test_sanitize_max_length(self):
        """Should respect max length parameter."""
        long_name = "a" * 200
        result = sanitize_filename(long_name, max_length=50)
        assert len(result) == 50
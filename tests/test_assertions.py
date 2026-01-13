"""
Tests for PyRate assertions module (fuzzy matchers).
"""
import pytest
from pyrate.assertions import Assertions
class TestFuzzyMatchers:
    """Test all fuzzy matcher types."""
    
    def test_notnull_matcher_passes_with_value(self):
        """#notnull should pass when value is not None."""
        Assertions.match("some value", "#notnull")
        Assertions.match(0, "#notnull")
        Assertions.match(False, "#notnull")
    
    def test_notnull_matcher_fails_with_none(self):
        """#notnull should fail when value is None."""
        with pytest.raises(AssertionError, match="Se esperaba #notnull"):
            Assertions.match(None, "#notnull")
    
    def test_null_matcher_passes_with_none(self):
        """#null should pass when value is None."""
        Assertions.match(None, "#null")
    
    def test_null_matcher_fails_with_value(self):
        """#null should fail when value is not None."""
        with pytest.raises(AssertionError, match="Se esperaba None"):
            Assertions.match("value", "#null")
    
    def test_string_matcher_passes_with_string(self):
        """#string should pass with string values."""
        Assertions.match("hello", "#string")
        Assertions.match("", "#string")
    
    def test_string_matcher_fails_with_non_string(self):
        """#string should fail with non-string values."""
        with pytest.raises(AssertionError, match="Se esperaba #string"):
            Assertions.match(123, "#string")
    
    def test_number_matcher_passes_with_numbers(self):
        """#number should pass with int and float."""
        Assertions.match(42, "#number")
        Assertions.match(3.14, "#number")
        Assertions.match(-1, "#number")
    
    def test_number_matcher_fails_with_non_number(self):
        """#number should fail with non-numeric values."""
        with pytest.raises(AssertionError, match="Se esperaba #number"):
            Assertions.match("123", "#number")
    
    def test_boolean_matcher_passes_with_bool(self):
        """#boolean should pass with boolean values."""
        Assertions.match(True, "#boolean")
        Assertions.match(False, "#boolean")
    
    def test_boolean_matcher_fails_with_non_bool(self):
        """#boolean should fail with non-boolean values."""
        with pytest.raises(AssertionError, match="Se esperaba #boolean"):
            Assertions.match(1, "#boolean")
    
    def test_array_matcher_passes_with_list(self):
        """#array should pass with list values."""
        Assertions.match([], "#array")
        Assertions.match([1, 2, 3], "#array")
    
    def test_array_matcher_fails_with_non_list(self):
        """#array should fail with non-list values."""
        with pytest.raises(AssertionError, match="Se esperaba #array"):
            Assertions.match({"key": "value"}, "#array")
    
    def test_object_matcher_passes_with_dict(self):
        """#object should pass with dictionary values."""
        Assertions.match({}, "#object")
        Assertions.match({"key": "value"}, "#object")
    
    def test_object_matcher_fails_with_non_dict(self):
        """#object should fail with non-dict values."""
        with pytest.raises(AssertionError, match="Se esperaba #object"):
            Assertions.match([1, 2, 3], "#object")
    
    def test_uuid_matcher_passes_with_valid_uuid(self):
        """#uuid should pass with valid UUID strings."""
        Assertions.match("550e8400-e29b-41d4-a716-446655440000", "#uuid")
    
    def test_uuid_matcher_fails_with_invalid_uuid(self):
        """#uuid should fail with invalid UUID strings."""
        with pytest.raises(AssertionError, match="no es un UUID válido"):
            Assertions.match("not-a-uuid", "#uuid")
    
    def test_ignore_matcher_always_passes(self):
        """#ignore should always pass regardless of value."""
        Assertions.match(None, "#ignore")
        Assertions.match("anything", "#ignore")
        Assertions.match(123, "#ignore")
class TestExactMatching:
    """Test exact value matching."""
    
    def test_exact_match_strings(self):
        """Exact match should work with identical strings."""
        Assertions.match("hello", "hello")
    
    def test_exact_match_numbers(self):
        """Exact match should work with identical numbers."""
        Assertions.match(42, 42)
        Assertions.match(3.14, 3.14)
    
    def test_exact_match_fails_with_different_values(self):
        """Exact match should fail with different values."""
        with pytest.raises(AssertionError, match="Valor incorrecto"):
            Assertions.match("hello", "world")
    
    def test_type_coercion_string_to_number(self):
        """Should handle string-number coercion."""
        Assertions.match(101, "101")
        Assertions.match("101", 101)

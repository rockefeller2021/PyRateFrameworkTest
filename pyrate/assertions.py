"""
Assertion utilities for PyRate Framework.

Provides flexible matchers including fuzzy matchers (inspired by Karate Framework)
for validating API responses and data structures.
"""

import re
from typing import Any


class Assertions:
    """
    Assertion utilities with support for fuzzy matchers.
    
    Fuzzy matchers allow type-based validation without exact value matching:
    - #notnull: Value must not be None
    - #null: Value must be None
    - #string: Value must be a string
    - #number: Value must be a number (int or float)
    - #boolean: Value must be a boolean
    - #array: Value must be a list
    - #object: Value must be a dictionary
    - #uuid: Value must be a valid UUID string
    - #ignore: Skip validation (always passes)
    
    Example:
        >>> Assertions.match(response.id, "#notnull")  # Just check it exists
        >>> Assertions.match(response.name, "John Doe")  # Exact match
        >>> Assertions.match(response.uuid, "#uuid")  # UUID validation
    """
    
    @staticmethod
    def match(actual: Any, expected: Any) -> None:
        """
        Match actual value against expected value or fuzzy matcher.
        
        Args:
            actual: The actual value to validate
            expected: Expected value or fuzzy matcher (e.g., #notnull, #string)
            
        Raises:
            AssertionError: If validation fails
            
        Examples:
            >>> # Exact matching
            >>> Assertions.match("hello", "hello")  # Passes
            >>> Assertions.match(200, "200")  # Passes (auto-conversion)
            
            >>> # Fuzzy matching
            >>> Assertions.match("test@example.com", "#string")  # Passes
            >>> Assertions.match(None, "#notnull")  # Raises AssertionError
            >>> Assertions.match(42, "#number")  # Passes
        """
        # 1. Validación de marcadores mágicos (Fuzzy Matchers)
        if isinstance(expected, str) and expected.startswith('#'):
            marker = expected.lower().strip()

            if marker == '#notnull':
                assert actual is not None, f"Se esperaba #notnull, pero llegó None"
                return
            elif marker == '#null':
                assert actual is None, f"Se esperaba None, pero llegó {actual}"
                return
            elif marker == '#string':
                assert isinstance(actual, str), f"Se esperaba #string, llegó {type(actual)}"
                return
            elif marker == '#number':
                assert isinstance(actual, (int, float)), f"Se esperaba #number, llegó {type(actual)}"
                return
            elif marker == '#boolean':
                assert isinstance(actual, bool), f"Se esperaba #boolean, llegó {type(actual)}"
                return
            elif marker == '#array':
                assert isinstance(actual, list), f"Se esperaba #array, llegó {type(actual)}"
                return
            elif marker == '#object':
                assert isinstance(actual, dict), f"Se esperaba #object, llegó {type(actual)}"
                return
            elif marker == '#uuid':
                uuid_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
                assert isinstance(actual, str) and re.match(uuid_regex,
                                                            actual), f"El valor '{actual}' no es un UUID válido"
                return
            elif marker == '#ignore':
                return  # No hacemos nada, pasa siempre

        # 2. Validación exacta (valores normales)
        if actual != expected:
            # Intento de conversión simple por si llega "101" vs 101
            if str(actual) == str(expected):
                return
            raise AssertionError(
                f"Valor incorrecto. Esperado: '{expected}' ({type(expected)}) | Recibido: '{actual}' ({type(actual)})")
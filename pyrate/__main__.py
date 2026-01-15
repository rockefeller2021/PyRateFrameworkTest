"""
PyRate Framework CLI Entry Point
=================================

This module allows running PyRate as a module:
    python -m pyrate --version
    python -m pyrate init
    python -m pyrate run tests/features/test.feature
"""

from .cli import main

if __name__ == "__main__":
    main()

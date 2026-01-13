# PyRate Framework

[![PyPI version](https://badge.fury.io/py/pyrate-framework.svg)](https://badge.fury.io/py/pyrate-framework)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyrate-framework.svg)](https://pypi.org/project/pyrate-framework/)
[![CI/CD](https://github.com/yourusername/pyrate/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/pyrate/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/yourusername/pyrate/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/pyrate)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Note**: Update GitHub URLs above with your actual repository information

## Commands to Run

```bash
# Run tests locally
python -m pytest tests/ -v --cov=pyrate

# Generate coverage report
python -m pytest tests/ --cov=pyrate --cov-report=html

# Run linting
flake8 pyrate/
black pyrate/ --check

# Format code
black pyrate/ tests/

# Type checking
mypy pyrate/ --ignore-missing-imports
```

## CI/CD Status

This project uses GitHub Actions for continuous integration and testing across Python 3.8-3.12.

View workflow: `.github/workflows/ci.yml`

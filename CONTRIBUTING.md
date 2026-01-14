# Contributing to PyRate Framework

Thank you for your interest in contributing to PyRate! This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 🤝 Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors. Be respectful, constructive, and professional in all interactions.

---

## 💡 How Can I Contribute?

### Reporting Bugs

Before creating a bug report:

- Check existing [issues](https://github.com/rockefeller2021/PyRateFrameworkTest/issues)
- Use the latest version of PyRate
- Include reproduction steps, expected vs actual behavior
- Provide system information (Python version, OS)

### Suggesting Features

Feature requests are welcome! Please:

- Check if the feature already exists or is planned
- Clearly describe the use case and benefits
- Provide examples if possible

### Code Contributions

1. **Small fixes** (typos, docs) - Create PR directly
2. **New features** - Open an issue first to discuss
3. **Bug fixes** - Reference the issue number in your PR

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- pip

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/PyRateFrameworkTest.git
cd PyRateFrameworkTest

# 2. Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# 3. Install in editable mode with dev dependencies
pip install -e .
pip install pytest pytest-cov black flake8 mypy

# 4. Install Playwright browsers
playwright install chromium

# 5. Run tests to verify setup
pytest tests/ -v
```

---

## 📏 Coding Standards

### Style

- **PEP 8** compliance (enforced by flake8)
- **Black** for code formatting (line length: 120)
- **Type hints** for all function signatures
- **Docstrings** for all public functions/classes

### Example

```python
def process_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Process an HTTP request and return the response.

    Args:
        url: Target URL for the request
        method: HTTP method (GET, POST, etc.)
        headers: Optional custom headers

    Returns:
        Dictionary containing response data

    Raises:
        ApiConnectionError: If request fails

    Examples:
        >>> process_request("https://api.example.com/users")
        {'status': 200, 'data': [...]}
    """
    # Implementation
```

### Code Quality Checks

```bash
# Format code
black pyrate/ tests/

# Check linting
flake8 pyrate/

# Type checking
mypy pyrate/ --ignore-missing-imports
```

---

## 🧪 Testing Guidelines

### Writing Tests

- **Location**: `tests/test_<module_name>.py`
- **Naming**: `test_<functionality>_<condition>`
- **Coverage**: Aim for >80%

### Test Structure

```python
import pytest
from pyrate.module import function_to_test

class TestFeatureName:
    """Test suite for feature X."""

    def test_basic_functionality(self):
        """Should return Y when given X."""
        # Arrange
        input_data = "test"

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result == "expected"

    def test_error_handling(self):
        """Should raise error for invalid input."""
        with pytest.raises(ValueError, match="error message"):
            function_to_test(invalid_input)
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_validators.py -v

# With coverage
pytest tests/ --cov=pyrate --cov-report=html
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Create a feature branch**

   ```bash
   git checkout develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

   - Write code following our standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Run quality checks**

   ```bash
   # Format
   black pyrate/ tests/

   # Lint
   flake8 pyrate/

   # Type check
   mypy pyrate/ --ignore-missing-imports

   # Tests
   pytest tests/ -v
   ```

4. **Commit with conventional commits**
   ```bash
   git commit -m "feat: add retry logic for API requests"
   git commit -m "fix: resolve timeout issue in browser tests"
   git commit -m "docs: update README with new examples"
   ```

### Commit Message Format

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Submitting PR

1. Push your branch

   ```bash
   git push origin feature/your-feature-name
   ```

2. Open Pull Request on GitHub

   - Target: `develop` branch
   - Title: Clear, descriptive summary
   - Description: What, why, how

3. PR Checklist
   - [ ] Tests pass locally
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)
   - [ ] Reviewed own code

### After Submission

- Respond to review comments promptly
- Make requested changes if needed
- Keep PR updated with `develop` branch

---

## 📂 Project Structure

```
PyRateProject/
├── pyrate/                 # Main package
│   ├── __init__.py
│   ├── core.py            # Core execution engine
│   ├── assertions.py      # Fuzzy matchers
│   ├── config.py          # Configuration
│   ├── validators.py      # Input validation
│   └── ...
├── tests/                 # Test suite
│   ├── test_assertions.py
│   ├── test_validators.py
│   └── ...
├── examples/              # Example feature files
├── .github/
│   └── workflows/
│       └── ci.yml        # CI/CD pipeline
├── setup.py              # Package setup
├── README.md
├── CHANGELOG.md
└── CONTRIBUTING.md       # This file
```

---

## 🎯 Good First Issues

Looking to contribute but don't know where to start?

- Look for issues tagged with `good first issue`
- Documentation improvements
- Adding examples
- Writing tests
- Fixing typos

---

## 📞 Getting Help

- **Questions**: Open a [discussion](https://github.com/rockefeller2021/PyRateFrameworkTest/discussions)
- **Bugs**: Open an [issue](https://github.com/rockefeller2021/PyRateFrameworkTest/issues)
- **Chat**: (Add Discord/Slack link if available)

---

## 🙏 Thank You!

Your contributions make PyRate better for everyone. We appreciate your time and effort!

---

**Happy Coding!** 🚀

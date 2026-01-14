# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-01-13

### 🎉 First Stable Release

PyRate Framework v1.0.0 is now production-ready! This release includes a complete automation testing framework for API and UI testing with Gherkin syntax.

### ✨ Added

#### Core Framework

- **Gherkin-based DSL** for readable test scenarios (`.feature` files)
- **API Testing** with full HTTP methods support (GET, POST, PUT, PATCH, DELETE)
- **UI Testing** with Playwright integration (Chromium, Firefox, WebKit)
- **Data-Driven Testing** with CSV, Excel, and JSON support
- **Fuzzy Matchers** inspired by Karate Framework (#notnull, #string, #number, #uuid, etc.)
- **Variable Injection** with `${variable}` syntax
- **Evidence Generation** with screenshots and API request/response logs
- **HTML Reports** with interactive charts and test case metrics

#### Configuration System

- **YAML Configuration** (`pyrate.config.yaml`) for centralized settings
- **Configurable timeouts** for API and browser operations
- **Custom headers** and SSL verification options
- **Headless/headful** browser mode configuration
- **Retry logic** configuration

#### Documentation

- **Comprehensive README** with installation, quickstart, and examples
- **Spanish Documentation** (README_ES.md)
- **Testing Guide** (TESTING.md) with pytest instructions
- **Selector Guide** for UI testing best practices
- **GitHub Setup Guide** for repository management

#### Testing & Quality

- **63 Unit Tests** with pytest (100% passing)
- **Python 3.8-3.12** compatibility
- **GitHub Actions CI/CD** with automatic testing
- **Code Coverage** reporting with pytest-cov
- **Linting** with flake8
- **Type Checking** with mypy
- **Code Formatting** with black

#### CLI

- `pyrate run <feature_file>` - Execute test scenarios
- `pyrate validate <feature_file>` - Validate Gherkin syntax
- `pyrate generate-config` - Generate example configuration
- `pyrate --version` - Show version information

### 🔧 Fixed

- **Python 3.8-3.11 compatibility** - Fixed f-string syntax errors
- **Flake8 configuration** - Removed invalid inline comments
- **Line ending consistency** - Added .gitattributes for cross-platform compatibility

### 📚 Documentation

- Complete API and UI testing examples
- SauceDemo integration example
- JSONPlaceholder API example
- Configuration YAML documentation
- Contribution guidelines

### 🏗️ Infrastructure

- GitHub Actions workflow for CI/CD
- Automated testing across Python versions
- Coverage reporting integration
- Package build verification

---

## [0.1.0] - 2025-12-15

### 🚀 Initial Development Release

- Basic framework structure
- Core Gherkin parser
- API request handling
- Playwright integration
- Evidence generation
- HTML report generation

---

## Release Notes

### v1.0.0 Highlights

**What's New:**

- ✅ Production-ready framework for API and UI testing
- ✅ 63 comprehensive unit tests
- ✅ Full Python 3.8-3.12 support
- ✅ GitHub Actions CI/CD pipeline
- ✅ Complete documentation in English and Spanish

**Breaking Changes:**

- None (first stable release)

**Upgrade Guide:**

- This is the first stable release. No migration needed.

**Known Issues:**

- `--version` flag requires workaround: use `pyrate -v` instead
- Browser evidence requires Playwright browser installation

**Roadmap for v1.1.0:**

- Enhanced retry logic for API requests
- JSON report generation
- GraphQL API support
- Performance improvements
- Additional fuzzy matchers

---

## Support

- **GitHub Issues**: [Report bugs](https://github.com/rockefeller2021/PyRateFrameworkTest/issues)
- **Documentation**: [README](https://github.com/rockefeller2021/PyRateFrameworkTest#readme)
- **Examples**: [examples/](https://github.com/rockefeller2021/PyRateFrameworkTest/tree/develop/examples)

---

**Full Changelog**: https://github.com/rockefeller2021/PyRateFrameworkTest/commits/main

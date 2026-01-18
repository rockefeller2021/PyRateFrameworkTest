# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0-beta.3] - 2026-01-17

### Added

- **Scroll Commands**: Complete scroll functionality for UI automation
  - `scroll to element` - Scroll to specific element (CSS or XPath)
  - `scroll to top` - Scroll to top of page
  - `scroll to bottom` - Scroll to bottom of page
  - `scroll to X, Y` - Scroll to specific coordinates
- **Dropdown/Select Commands**: Three methods for dropdown selection
  - `select SELECTOR by text TEXT` - Select by visible text
  - `select SELECTOR by value VALUE` - Select by value attribute
  - `select SELECTOR by index INDEX` - Select by zero-based index
- **Checkbox Commands**: Complete checkbox control
  - `check SELECTOR` - Check a checkbox
  - `uncheck SELECTOR` - Uncheck a checkbox
  - `toggle SELECTOR` - Toggle checkbox state
- **Radio Button Commands**: Radio button selection
  - `check radio SELECTOR` - Select a radio button
- **Iframe Commands**: Navigate between iframes and main page
  - `switch to frame SELECTOR` - Switch to iframe by selector or index
  - `switch to default content` / `switch to main` - Return to main page
  - `switch to parent` - Return to parent frame
  - Added `_main_page` attribute to store main page reference
- **Popup/Alert Commands**: Handle JavaScript dialogs
  - `accept alert` - Accept alert/confirm dialog
  - `dismiss alert` - Dismiss alert/confirm dialog
  - `match alert text == TEXT` - Validate alert message
  - `type in prompt TEXT` - Type text in prompt dialog

### Technical Details

- **Total New Commands**: 26 new Gherkin commands
- **Lines Added**: 187 lines of production code in `core.py`
- **XPath Support**: All new commands support both CSS and XPath selectors
- **File Changes**: Modified `pyrate/core.py` (lines 46, 454, 494-678)
- **Test Coverage**: 25 integration tests across 6 test files
- **Backward Compatibility**: 100% compatible with v1.1.0-beta.2

### Examples

```gherkin
# Scroll commands
And scroll to element '#footer'
And scroll to top
And scroll to 500, 1000

# Dropdown selection
And select '#country' by text 'United States'
And select '#country' by value 'US'
And select '#country' by index 0

# Checkbox operations
And check '#terms'
And uncheck '#newsletter'
And toggle '#remember-me'

# Radio buttons
And check radio '#gender-male'

# Iframes
And switch to frame '#payment-iframe'
And switch to default content

# Alerts
And accept alert
Then match alert text == 'Are you sure?'
And type in prompt 'John Doe'
```

### Testing

- `tests/test_scroll.py` - 5 scroll tests
- `tests/test_dropdowns.py` - 4 dropdown tests
- `tests/test_checkboxes.py` - 4 checkbox tests
- `tests/test_radio.py` - 3 radio button tests
- `tests/test_iframes.py` - 4 iframe tests
- `tests/test_alerts.py` - 5 alert/popup tests

---

## [1.1.0-beta.1] - 2026-01-17

### Added

- **XPath Selector Support**: UI automation now supports XPath expressions alongside CSS selectors
  - Auto-detection: XPath expressions starting with `//` or `/` are automatically detected
  - Explicit prefix: Use `xpath=//your/xpath` for explicit XPath selectors
  - Backward compatible: All existing CSS selectors continue to work unchanged
  - Updated commands: `input`, `click`, and `match text` now support both CSS and XPath
  - New module: `pyrate/selectors.py` with `SelectorStrategy` class
  - 18 comprehensive unit tests in `tests/test_selectors.py`
  - Example file: `examples/xpath_selectors.feature`
  - Documentation: Updated README.md and README_ES.md with XPath examples

### Technical Details

- `SelectorStrategy.parse()` - Automatic selector type detection
- `SelectorStrategy.validate()` - Selector syntax validation
- `SelectorStrategy.format_for_playwright()` - Playwright API formatting
- 100% backward compatibility with v1.0.2

### Examples

```gherkin
# CSS (existing, works unchanged)
And input '#username' 'admin'

# XPath with prefix
And input 'xpath=//input[@id="username"]' 'admin'

# XPath auto-detected
And input '//input[@id="username"]' 'admin'
```

---

## [1.1.0-beta.2] - 2026-01-17

### Added

- **Descriptive Gherkin Syntax**: Optional human-readable descriptions before commands for clearer evidence generation
  - Add comments before commands to describe actions in plain language
  - Descriptions appear in evidence reports instead of raw Gherkin syntax
  - Tag comments (`# @smoke`) are NOT captured as descriptions
  - Backward compatible: All existing tests work without changes
  - 14 comprehensive unit tests in `tests/test_descriptive_syntax.py`
  - Example file: `examples/descriptive_syntax.feature`
  - Documentation: Updated README.md and README_ES.md with syntax examples

### Technical Details

- Modified `_execute_lines()` in `core.py` to capture comment-based descriptions
- Added `pending_description` variable to track descriptions for next command
- Added regex filtering to distinguish tags from descriptions
- Added `raw_command` field to `step_record` for technical reference
- 100% backward compatibility with v1.0.2

### Examples

```gherkin
# Navigate to login page    ← Description
Given driver 'https://www.saucedemo.com'

# Enter username    ← Description
And input '#user' 'admin'

And click '#login'    ← No description (uses command)
```

**Evidence Output:**

```
Step 1: Navigate to login page ✅
Step 2: Enter username ✅
Step 3: And click '#login' ✅
```

---

## [1.1.0-beta.1] - 2026-01-17

## [1.0.2] - 2026-01-14

### 🔧 Fixed

- **CLI Entry Point**: Added `__main__.py` to enable `python -m pyrate` execution pattern
- **Argument Parsing**: Fixed CLI to properly handle `--version` flag and show help when no subcommand is provided
- **Metadata**: Corrected repository URLs in `setup.py` from placeholder to actual GitHub repository
- **Author Information**: Updated author metadata in `__init__.py` with correct name and documentation links

### 📦 Package Distribution

- **MANIFEST.in**: Created manifest file to ensure documentation, examples, and license files are included in PyPI distribution
- **Automated Publishing**: Added GitHub Actions workflow for automatic PyPI publishing using Trusted Publishers (OIDC)

### 📚 Documentation

- **PyPI Badges**: Added PyPI version and download badges to README
- **Contact Information**: Updated README with actual author contact details
- **Repository Links**: Fixed all GitHub repository URLs across documentation

### ⚡ Improvements

- Better CLI user experience with helpful error messages
- Enhanced package metadata for PyPI discoverability
- Professional GitHub Actions CI/CD pipeline for releases

---

## [1.0.1] - 2026-01-14

### 🚀 TestPyPI Release

- Successfully published to TestPyPI for validation
- Initial public release testing

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

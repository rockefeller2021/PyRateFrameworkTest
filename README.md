# 🚀 PyRate Framework

**English | [Español](README_ES.md)**

[![PyPI version](https://img.shields.io/pypi/v/pyrate-framework.svg)](https://pypi.org/project/pyrate-framework/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pyrate-framework.svg)](https://pypi.org/project/pyrate-framework/)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![CI/CD](https://github.com/rockefeller2021/PyRateFrameworkTest/actions/workflows/ci.yml/badge.svg)](https://github.com/rockefeller2021/PyRateFrameworkTest/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Automation testing framework for API and UI inspired by Karate Framework**

PyRate combines the simplicity of Gherkin-style syntax with the power of Python, Playwright, and Requests to create a unified testing framework for both API and UI automation.

---

## ✨ Features

- 🎯 **Natural Language Syntax** - Write tests in Gherkin-style format
- 🌐 **API Testing** - Full REST API support with `requests`
- 🖥️ **UI Testing** - Browser automation with `playwright`
- 📊 **Data-Driven Testing** - CSV, Excel, and JSON data sources
- 📄 **Evidence Generation** - Automatic DOCX and TXT reports
- 📈 **Beautiful HTML Reports** - Interactive dashboards with screenshots
- 🎭 **Fuzzy Matchers** - Flexible assertions (`#notnull`, `#uuid`, etc.)
- 🔄 **Modular Execution** - Reuse test scenarios with `call read()`

---

## 🚀 Quick Start

### Installation

```bash
pip install pyrate-framework
playwright install chromium
```

### Create Your First Test

1. **Initialize a project:**

```bash
pyrate init
```

This creates:

```
your-project/
├── tests/
│   ├── features/
│   │   └── demo.feature
│   └── data/
├── reports/
└── .env
```

2. **Write a test** (`tests/features/api_test.feature`):

```gherkin
# @smoke @api
Given url 'https://jsonplaceholder.typicode.com'
And path 'users/1'
When method get
Then status 200
And match response.name == 'Leanne Graham'
And match response.id == #notnull
```

3. **Run the test:**

```bash
pyrate run tests/features/api_test.feature
```

4. **View the report:**

Open `reports/ultimo_reporte.html` in your browser 🎉

---

## ⚙️ Configuration (Optional)

PyRate works **out-of-the-box** with sensible defaults. Configuration is **optional** but allows you to customize behavior for different environments (local, CI/CD, staging, etc.).

### 🚀 Quick Start (No Configuration Needed)

```bash
pyrate run tests/features/test.feature  # ✅ Uses intelligent defaults
```

### 📝 Custom Configuration (Advanced Users)

#### Step 1: Generate Example Configuration

When you run `pyrate init`, it automatically creates a configuration example:

```bash
pyrate init
# Creates: pyrate.config.yaml.example
```

#### Step 2: Create Your Configuration

```bash
# Copy the example file
cp pyrate.config.yaml.example pyrate.config.yaml

# Edit with your preferred settings
```

#### Step 3: Use Custom Configuration

```bash
# Use specific config file
pyrate run tests/features/test.feature -c pyrate.config.yaml

# Or place pyrate.config.yaml in project root (auto-detected)
pyrate run tests/features/test.feature
```

---

### 📋 Complete Configuration Reference

Here's a **fully documented YAML configuration** with all available options:

```yaml
pyrate:
  # ========================================
  # Evidence Generation Settings
  # ========================================
  evidence:
    folder: "evidence" # Directory for evidence files
    screenshot_on_pass: true # Capture screenshots on successful UI steps
    screenshot_on_fail: true # Capture screenshots on failed steps

  # ========================================
  # HTML Report Settings
  # ========================================
  reports:
    folder: "reports" # Directory for HTML/JSON reports

  # ========================================
  # Browser Automation (Playwright)
  # ========================================
  browser:
    headless:
      false # Run browser in headless mode
      # Set to 'true' for CI/CD environments
    timeout:
      30000 # Browser operation timeout (milliseconds)
      # Default: 30 seconds

  # ========================================
  # API Testing Settings
  # ========================================
  api:
    timeout: 30 # HTTP request timeout (seconds)
    verify_ssl:
      true # Verify SSL certificates
      # Set to 'false' for self-signed certs
    retry_attempts:
      1 # Number of retry attempts for failed requests
      # Useful for flaky endpoints
    retry_delay: 1.0 # Delay between retries (seconds)
    user_agent: "PyRate/1.0" # Custom User-Agent header

  # ========================================
  # Logging Settings
  # ========================================
  logging:
    verbose: false # Enable verbose/debug logging
    max_response_size: 500 # Max response data to log (characters)
```

---

### 🎯 Configuration Examples

#### Example 1: CI/CD Environment (GitHub Actions, Jenkins)

```yaml
pyrate:
  browser:
    headless: true # ✅ No GUI in CI
    timeout: 60000 # ⏱️ Longer timeout for slow CI machines

  api:
    retry_attempts: 3 # 🔁 Retry flaky network requests
    timeout: 60

  logging:
    verbose: true # 🐛 Debug logs for CI troubleshooting
```

**Usage**:

```bash
pyrate run tests/ -c ci-config.yaml
```

---

#### Example 2: Local Development

```yaml
pyrate:
  browser:
    headless: false # 👀 See browser for debugging
    timeout: 30000

  evidence:
    screenshot_on_pass: false # 📸 Only capture failures to save space

  api:
    verify_ssl: false # 🔓 Allow self-signed certs (localhost)
```

---

#### Example 3: Staging/QA Environment

```yaml
pyrate:
  browser:
    headless: true
    timeout: 45000 # ⏱️ Moderate timeout

  api:
    retry_attempts: 5 # 🔁 High retry for unstable staging
    retry_delay: 2.0
    verify_ssl: true

  evidence:
    folder: "staging_evidence" # 📁 Separate evidence per environment

  reports:
    folder: "staging_reports"
```

---

### 💡 Configuration Priority

PyRate loads configuration in this order (later overrides earlier):

1. **Built-in defaults** (in `pyrate/config.py`)
2. **`pyrate.config.yaml`** in current directory (auto-detected)
3. **Environment variables** (if present)
4. **Config file** specified with `-c` flag (highest priority)

---

## 🎯 UI Selectors

PyRate supports both **CSS selectors** and **XPath expressions** for UI automation. The framework automatically detects which type you're using.

### CSS Selectors (Default)

Use standard CSS selectors for most UI interactions:

```gherkin
# By ID
And input '#username' 'john_doe'

# By class
And click '.btn-primary'

# By attribute
And input 'input[name="email"]' 'john@example.com'

# Complex selectors
And click 'button[type="submit"].login-btn'
```

### XPath Selectors

For complex DOM navigation or dynamic elements, use XPath:

#### Option 1: Explicit Prefix

```gherkin
# With xpath= prefix
And input 'xpath=//input[@id="username"]' 'john_doe'
And click 'xpath=//button[@type="submit"]'
Then match text 'xpath=//h1[@class="welcome"]' == 'Welcome'
```

#### Option 2: Auto-Detection

```gherkin
# XPath starting with // or / is auto-detected
And input '//input[@id="username"]' 'john_doe'
And click '//button[text()="Login"]'
Then match text '//h1' == 'Welcome'
```

### Advanced XPath Examples

```gherkin
# Contains text
And click '//button[contains(text(), "Submit")]'

# By data attributes (recommended for testing)
And input '//input[@data-testid="username-field"]' 'admin'

# Navigate hierarchy
And input '//form[@name="login"]//input[@type="password"]' 'secret'

# Multiple conditions
And click '//button[@type="submit" and contains(@class, "primary")]'

# By index
And input '(//input[@type="text"])[2]' 'second-input'
```

### Mixing CSS and XPath

You can use both in the same test:

```gherkin
And input '#username' 'admin'  # CSS
And input '//input[@id="password"]' 'pass123'  # XPath
And click '.submit-btn'  # CSS
Then match text '//div[@class="message"]' == 'Success'  # XPath
```

---

Example:

```bash
# Uses pyrate.config.yaml if exists, otherwise defaults
pyrate run test.feature

# Explicitly use custom config (overrides pyrate.config.yaml)
pyrate run test.feature -c production.yaml
```

---

### 🔧 Advanced: Programmatic Configuration

You can also configure PyRate programmatically:

```python
from pyrate import PyRateRunner
from pyrate.config import PyRateConfig

# Create custom config
config = PyRateConfig(
    headless=True,
    api_timeout=60,
    retry_attempts=5,
    evidence_folder="custom_evidence"
)

# Use in runner
runner = PyRateRunner(config=config)
runner.execute_file("tests/features/test.feature")
```

---

## 📖 Documentation

### API Testing Example

```gherkin
# @api
Scenario: Create a new post

Given url 'https://jsonplaceholder.typicode.com'
And path 'posts'
And header Content-Type = 'application/json'
And request { "title": "PyRate Test", "body": "Testing", "userId": 1 }
When method post
Then status 201
And match response.id == #notnull
And match response.title == 'PyRate Test'
```

### UI Testing Example

```gherkin
# @ui
Scenario: Login to application

Given driver 'https://example.com/login'
And input '#username' 'testuser'
And input '#password' 'password123'
And click 'button[type="submit"]'
And wait 2
Then match text 'h1' == 'Welcome'
```

### Data-Driven Testing

**data.csv:**

```csv
username,password
user1,pass1
user2,pass2
```

**test.feature:**

```gherkin
Data source: data.csv

Scenario: Login with multiple users
Given url 'https://api.example.com/login'
And request { "username": "#(username)", "password": "#(password)" }
When method post
Then status 200
```

---

## 🎯 Supported Commands

### API Testing

| Command       | Description           | Example                                     |
| ------------- | --------------------- | ------------------------------------------- |
| `Given url`   | Set base URL          | `Given url 'https://api.example.com'`       |
| `And path`    | Append path to URL    | `And path 'users/1'`                        |
| `And header`  | Set request header    | `And header Authorization = 'Bearer token'` |
| `And request` | Set request body      | `And request { "name": "John" }`            |
| `When method` | Execute HTTP method   | `When method post`                          |
| `Then status` | Assert status code    | `Then status 200`                           |
| `And match`   | Assert response field | `And match response.name == 'John'`         |

### UI Testing

| Command           | Description         | Example                              |
| ----------------- | ------------------- | ------------------------------------ |
| `Given driver`    | Open browser to URL | `Given driver 'https://example.com'` |
| `And input`       | Fill input field    | `And input '#username' 'testuser'`   |
| `And click`       | Click element       | `And click 'button.submit'`          |
| `And wait`        | Wait seconds        | `And wait 3`                         |
| `Then match text` | Assert element text | `Then match text 'h1' == 'Welcome'`  |

### Fuzzy Matchers

| Matcher    | Description        | Example                                   |
| ---------- | ------------------ | ----------------------------------------- |
| `#notnull` | Value is not null  | `And match response.id == #notnull`       |
| `#null`    | Value is null      | `And match response.deleted == #null`     |
| `#string`  | Value is a string  | `And match response.name == #string`      |
| `#number`  | Value is a number  | `And match response.age == #number`       |
| `#boolean` | Value is a boolean | `And match response.active == #boolean`   |
| `#array`   | Value is an array  | `And match response.items == #array`      |
| `#object`  | Value is an object | `And match response.user == #object`      |
| `#uuid`    | Value is a UUID    | `And match response.id == #uuid`          |
| `#ignore`  | Skip assertion     | `And match response.timestamp == #ignore` |

---

## 🔧 CLI Commands

```bash
# Initialize new project
pyrate init

# Run a single feature file
pyrate run tests/features/login.feature

# Run all features in a folder
pyrate run tests/features/

# Run with tag filtering
pyrate run tests/features/ -t @smoke

# Show version
pyrate --version
```

---

## 📊 Comparison with Karate Framework

| Feature            | Karate | PyRate | Status      |
| ------------------ | ------ | ------ | ----------- |
| Gherkin Syntax     | ✅     | ✅     | ✅          |
| API Testing        | ✅     | ✅     | ✅          |
| UI Testing         | ✅     | ✅     | ✅          |
| Data-Driven        | ✅     | ✅     | ✅          |
| Fuzzy Matchers     | ✅     | ✅     | ✅          |
| HTML Reports       | ✅     | ✅     | ✅          |
| Evidence DOCX      | ❌     | ✅     | **Unique!** |
| Configuration YAML | ✅     | ✅     | ✅          |
| Parallel Execution | ✅     | 🚧     | Roadmap     |

---

## 🛣️ Roadmap

- [x] **v1.0**: Configuration system with YAML ✅
- [ ] **v1.2**: Parallel scenario execution
- [ ] **v1.3**: JSON Schema validation
- [ ] **v1.4**: Mock server support
- [ ] **v2.0**: GraphQL support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by [Karate Framework](https://github.com/karatelabs/karate)
- Built with [Playwright](https://playwright.dev/) for UI automation
- Powered by [Requests](https://requests.readthedocs.io/) for API testing

---

## 📧 Contact

- **Author**: Rafael Enrique Alvarado García
- **Email**: magomlg@gmail.com
- **GitHub**: [@rockefeller2021](https://github.com/rockefeller2021)
- **PyPI**: [pyrate-framework](https://pypi.org/project/pyrate-framework/)

---

**Made with ❤️ for the testing community**

# 🧪 Testing Guide - PyRate Framework

Esta guía explica cómo ejecutar y escribir tests para PyRate Framework.

---

## 📋 Tabla de Contenidos

- [Ejecutar Tests](#ejecutar-tests)
- [Cobertura de Código](#cobertura-de-código)
- [Estructura de Tests](#estructura-de-tests)
- [Escribir Nuevos Tests](#escribir-nuevos-tests)
- [Linting y Formateo](#linting-y-formateo)

---

## 🚀 Ejecutar Tests

### Ejecutar Todos los Tests

```bash
pytest tests/
```

### Ejecutar con Verbose

```bash
pytest tests/ -v
```

### Ejecutar Tests Específicos

```bash
# Un archivo específico
pytest tests/test_assertions.py

# Una clase específica
pytest tests/test_assertions.py::TestFuzzyMatchers

# Un test específico
pytest tests/test_assertions.py::TestFuzzyMatchers::test_notnull_matcher_passes_with_value
```

---

## 📊 Cobertura de Código

### Ejecutar con Coverage

```bash
pytest tests/ --cov=pyrate --cov-report=html --cov-report=term
```

### Ver Reporte HTML

```bash
# Abre el archivo generado
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### Objetivo de Cobertura

Target: **≥ 80%** de cobertura

---

## 🗂️ Estructura de Tests

```
tests/
├── __init__.py
├── test_assertions.py      # Tests para fuzzy matchers
├── test_validators.py      # Tests para validaciones
├── test_config_loader.py   # Tests para configuración YAML
├── test_data_loader.py     # Tests para carga de datos
└── fixtures/               # Archivos de ejemplo (CSV, JSON, etc.)
```

---

## 📝 Módulos Testeados

### ✅ test_assertions.py

Cubre `pyrate/assertions.py`

**Tests incluidos**:

- `#notnull` - Validar valores no nulos
- `#null` - Validar valores nulos
- `#string` - Validar strings
- `#number` - Validar números
- `#boolean` - Validar booleanos
- `#array` - Validar arrays
- `#object` - Validar objetos/diccionarios
- `#uuid` - Validar UUIDs
- `#ignore` - Ignorar validación
- Exact matching - Coincidencias exactas

**Ejemplo**:

```python
def test_notnull_matcher_passes_with_value(self):
    """#notnull should pass when value is not None."""
    Assertions.match("some value", "#notnull")
    Assertions.match(0, "#notnull")
    Assertions.match(False, "#notnull")
```

---

### ✅ test_validators.py

Cubre `pyrate/validators.py`

**Tests incluidos**:

- `is_valid_url()` - URLs HTTP/HTTPS válidas
- `is_valid_json()` - JSON válido
- `is_valid_selector()` - Selectores CSS válidos
- `is_valid_http_method()` - Métodos HTTP (GET, POST, etc.)
- `is_valid_status_code()` - Códigos HTTP (200-599)
- `sanitize_filename()` - Sanitización de nombres de archivo

**Ejemplo**:

```python
def test_valid_https_url(self):
    """Should accept valid HTTPS URLs."""
    assert is_valid_url("https://example.com")
    assert is_valid_url("https://api.example.com/v1/users")
```

---

### ✅ test_config_loader.py

Cubre `pyrate/config.py` y `pyrate/config_loader.py`

**Tests incluidos**:

- Valores por defecto de configuración
- Validación de parámetros (timeouts positivos, retry ≥ 1)
- Carga desde diccionario (`from_dict`)
- Conversión a diccionario (`to_dict`)
- Carga desde archivo YAML
- Generación de ejemplo de configuración

**Ejemplo**:

```python
def test_load_from_yaml_file(self):
    """Should load configuration from YAML file."""
    yaml_content = """
pyrate:
  browser:
    headless: true
    timeout: 60000
"""
    # ... test implementation
```

---

### ✅ test_data_loader.py

Cubre `pyrate/data_loader.py`

**Tests incluidos**:

- Carga de archivos CSV
- Carga de archivos Excel (.xlsx)
- Carga de archivos JSON (array y objeto único)
- Manejo de errores (archivo no encontrado, formato no soportado)

**Ejemplo**:

```python
def test_load_valid_csv(self):
    """Should load valid CSV file."""
    csv_content = "username,password\\nuser1,pass1\\nuser2,pass2"
    # Creates temp file and validates loading
```

---

## ✍️ Escribir Nuevos Tests

### Template Básico

```python
import pytest
from pyrate.module_name import function_to_test


class TestFeatureName:
    """Test feature description."""

    def test_basic_functionality(self):
        """Should do X when Y."""
        # Arrange
        input_data = "test"

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result == "expected"

    def test_error_handling(self):
        """Should raise error when invalid input."""
        with pytest.raises(ValueError, match="error message"):
            function_to_test(invalid_input)
```

### Buenas Prácticas

1. **Naming**: Nombres descriptivos con `test_` prefix

   ```python
   def test_notnull_matcher_passes_with_value(self):  # ✅
   def test1(self):  # ❌
   ```

2. **Docstrings**: Descripción clara de qué testea

   ```python
   def test_valid_url(self):
       """Should accept valid HTTP and HTTPS URLs."""  # ✅
   ```

3. **AAA Pattern**: Arrange, Act, Assert

   ```python
   # Arrange - preparar datos
   url = "https://example.com"

   # Act - ejecutar función
   result = is_valid_url(url)

   # Assert - verificar resultado
   assert result is True
   ```

4. **Test Positivos y Negativos**:
   ```python
   def test_accepts_valid_input(self):  # ✅ caso positivo
   def test_rejects_invalid_input(self):  # ✅ caso negativo
   ```

---

## 🎨 Linting y Formateo

### Black (Formateo Automático)

```bash
# Formatear todo el código
black pyrate/ tests/

# Solo ver cambios (dry-run)
black --check pyrate/
```

### Flake8 (Validación de Estilo)

```bash
# Validar estilo
flake8 pyrate/

# Con configuración custom
flake8 pyrate/ --config=setup.cfg
```

### Mypy (Type Checking)

```bash
# Verificar tipos
mypy pyrate/

# Ignorar módulos sin tipos
mypy pyrate/ --ignore-missing-imports
```

### Todo en Uno

```bash
# Formatear + validar + verificar tipos
black pyrate/ tests/ && flake8 pyrate/ && mypy pyrate/
```

---

## 🔧 Configuración (setup.cfg)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short

[coverage:run]
source = pyrate
omit = */tests/*

[coverage:report]
precision = 2
show_missing = True

[flake8]
max-line-length = 120
exclude = .git,__pycache__,build,dist

[mypy]
python_version = 3.8
warn_return_any = True
ignore_missing_imports = True
```

---

## 📊 Reportes de Cobertura

### Terminal Output

```bash
pytest tests/ --cov=pyrate --cov-report=term

# Output:
# ---------- coverage: platform win32, python 3.12.0 ----------
# Name                      Stmts   Miss  Cover
# ---------------------------------------------
# pyrate/__init__.py           10      0   100%
# pyrate/assertions.py         50      5    90%
# pyrate/validators.py         60      3    95%
# ---------------------------------------------
# TOTAL                       120      8    93%
```

### HTML Report

```bash
pytest tests/ --cov=pyrate --cov-report=html

# Genera: htmlcov/index.html
# Muestra líneas cubiertas/no cubiertas con colores
```

---

## 🐛 Debugging Tests

### Modo Verbose con Stack Trace

```bash
pytest tests/ -vv --tb=long
```

### Detener en el Primer Error

```bash
pytest tests/ -x
```

### Ejecutar con PDB (Python Debugger)

```bash
pytest tests/ --pdb
```

### Ver Print Statements

```bash
pytest tests/ -s
```

---

## 🚀 CI/CD Integration

Los tests se ejecutan automáticamente en GitHub Actions en cada push.

Ver: `.github/workflows/ci.yml`

```yaml
- name: Run tests
  run: pytest tests/ --cov=pyrate --cov-report=xml
```

---

## 📚 Recursos Adicionales

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8](https://flake8.pycqa.org/)
- [Mypy](https://mypy.readthedocs.io/)

---

**Última actualización**: 2026-01-12

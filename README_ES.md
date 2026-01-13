# 🚀 PyRate Framework

**[English](README.md) | Español**

[![PyPI version](https://badge.fury.io/py/pyrate-framework.svg)](https://badge.fury.io/py/pyrate-framework)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyrate-framework.svg)](https://pypi.org/project/pyrate-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Framework de automatización de pruebas para API y UI inspirado en Karate Framework**

PyRate combina la simplicidad de la sintaxis estilo Gherkin con el poder de Python, Playwright y Requests para crear un framework unificado de automatización tanto para API como para UI.

---

## ✨ Características

- 🎯 **Sintaxis en Lenguaje Natural** - Escribe pruebas en formato estilo Gherkin
- 🌐 **Pruebas de API** - Soporte completo para REST API con `requests`
- 🖥️ **Pruebas de UI** - Automatización del navegador con `playwright`
- 📊 **Pruebas Data-Driven** - Fuentes de datos CSV, Excel y JSON
- 📄 **Generación de Evidencias** - Reportes automáticos en DOCX y TXT
- 📈 **Reportes HTML Hermosos** - Dashboards interactivos con capturas de pantalla
- 🎭 **Fuzzy Matchers** - Aserciones flexibles (`#notnull`, `#uuid`, etc.)
- 🔄 **Ejecución Modular** - Reutiliza escenarios de prueba con `call read()`

---

## 🚀 Inicio Rápido

### Instalación

```bash
pip install pyrate-framework
playwright install chromium
```

### Crea Tu Primera Prueba

1. **Inicializa un proyecto:**

```bash
pyrate init
```

Esto crea:

```
tu-proyecto/
├── tests/
│   ├── features/
│   │   └── demo.feature
│   └── data/
├── reports/
├── .env
└── pyrate.config.yaml.example
```

2. **Escribe una prueba** (`tests/features/api_test.feature`):

```gherkin
# @smoke @api
Given url 'https://jsonplaceholder.typicode.com'
And path 'users/1'
When method get
Then status 200
And match response.name == 'Leanne Graham'
And match response.id == #notnull
```

3. **Ejecuta la prueba:**

```bash
pyrate run tests/features/api_test.feature
```

4. **Ve el reporte:**

Abre `reports/ultimo_reporte.html` en tu navegador 🎉

---

## ⚙️ Configuración (Opcional)

PyRate funciona **de inmediato** con valores predeterminados sensibles. La configuración es **opcional** pero te permite personalizar el comportamiento para diferentes entornos (local, CI/CD, staging, etc.).

### 🚀 Inicio Rápido (Sin Configuración Necesaria)

```bash
pyrate run tests/features/test.feature  # ✅ Usa valores inteligentes por defecto
```

### 📝 Configuración Personalizada (Usuarios Avanzados)

#### Paso 1: Genera la Configuración de Ejemplo

Cuando ejecutas `pyrate init`, automáticamente crea un ejemplo de configuración:

```bash
pyrate init
# Crea: pyrate.config.yaml.example
```

#### Paso 2: Crea Tu Configuración

```bash
# Copia el archivo de ejemplo
cp pyrate.config.yaml.example pyrate.config.yaml

# Edita con tus configuraciones preferidas
```

#### Paso 3: Usa la Configuración Personalizada

```bash
# Usa un archivo de configuración específico
pyrate run tests/features/test.feature -c pyrate.config.yaml

# O coloca pyrate.config.yaml en la raíz del proyecto (auto-detectado)
pyrate run tests/features/test.feature
```

---

### 📋 Referencia Completa de Configuración

Aquí está una **configuración YAML totalmente documentada** con todas las opciones disponibles:

```yaml
pyrate:
  # ========================================
  # Configuración de Generación de Evidencias
  # ========================================
  evidence:
    folder: "evidence" # Directorio para archivos de evidencia
    screenshot_on_pass: true # Capturar capturas en pasos UI exitosos
    screenshot_on_fail: true # Capturar capturas en pasos fallidos

  # ========================================
  # Configuración de Reportes HTML
  # ========================================
  reports:
    folder: "reports" # Directorio para reportes HTML/JSON

  # ========================================
  # Automatización del Navegador (Playwright)
  # ========================================
  browser:
    headless:
      false # Ejecutar navegador en modo headless
      # Establece 'true' para entornos CI/CD
    timeout:
      30000 # Timeout de operaciones del navegador (milisegundos)
      # Por defecto: 30 segundos

  # ========================================
  # Configuración de Pruebas API
  # ========================================
  api:
    timeout: 30 # Timeout de peticiones HTTP (segundos)
    verify_ssl:
      true # Verificar certificados SSL
      # Establece 'false' para certificados autofirmados
    retry_attempts:
      1 # Número de reintentos para peticiones fallidas
      # Útil para endpoints inestables
    retry_delay: 1.0 # Demora entre reintentos (segundos)
    user_agent: "PyRate/1.0" # Header User-Agent personalizado

  # ========================================
  # Configuración de Logging
  # ========================================
  logging:
    verbose: false # Habilitar logging verbose/debug
    max_response_size: 500 # Máx. datos de respuesta a loguear (caracteres)
```

---

### 🎯 Ejemplos de Configuración

#### Ejemplo 1: Entorno CI/CD (GitHub Actions, Jenkins)

```yaml
pyrate:
  browser:
    headless: true # ✅ Sin GUI en CI
    timeout: 60000 # ⏱️ Timeout mayor para máquinas CI lentas

  api:
    retry_attempts: 3 # 🔁 Reintentar peticiones de red inestables
    timeout: 60

  logging:
    verbose: true # 🐛 Logs de debug para troubleshooting en CI
```

**Uso**:

```bash
pyrate run tests/ -c ci-config.yaml
```

---

#### Ejemplo 2: Desarrollo Local

```yaml
pyrate:
  browser:
    headless: false # 👀 Ver navegador para debugging
    timeout: 30000

  evidence:
    screenshot_on_pass: false # 📸 Solo capturar fallos para ahorrar espacio

  api:
    verify_ssl: false # 🔓 Permitir certificados autofirmados (localhost)
```

---

#### Ejemplo 3: Entorno Staging/QA

```yaml
pyrate:
  browser:
    headless: true
    timeout: 45000 # ⏱️ Timeout moderado

  api:
    retry_attempts: 5 # 🔁 Alto retry para staging inestable
    retry_delay: 2.0
    verify_ssl: true

  evidence:
    folder: "staging_evidence" # 📁 Evidencia separada por entorno

  reports:
    folder: "staging_reports"
```

---

### 💡 Prioridad de Configuración

PyRate carga la configuración en este orden (lo posterior sobreescribe lo anterior):

1. **Valores por defecto** (en `pyrate/config.py`)
2. **`pyrate.config.yaml`** en directorio actual (auto-detectado)
3. **Archivo personalizado** vía flag `-c/--config` (máxima prioridad)

Ejemplo:

```bash
# Usa pyrate.config.yaml si existe, sino valores por defecto
pyrate run test.feature

# Usa explícitamente config personalizado (sobreescribe pyrate.config.yaml)
pyrate run test.feature -c production.yaml
```

---

### 🔧 Avanzado: Configuración Programática

También puedes configurar PyRate programáticamente:

```python
from pyrate import PyRateRunner
from pyrate.config import PyRateConfig

# Crear configuración personalizada
config = PyRateConfig(
    headless=True,
    api_timeout=60,
    retry_attempts=5,
    evidence_folder="evidencia_personalizada"
)

# Usar en el runner
runner = PyRateRunner(config=config)
runner.execute_file("tests/features/test.feature")
```

---

## 📖 Documentación

### Ejemplo de Prueba API

```gherkin
# @api
Scenario: Crear un nuevo post

Given url 'https://jsonplaceholder.typicode.com'
And path 'posts'
And header Content-Type = 'application/json'
And request { "title": "PyRate Test", "body": "Testing", "userId": 1 }
When method post
Then status 201
And match response.id == #notnull
And match response.title == 'PyRate Test'
```

### Ejemplo de Prueba UI

```gherkin
# @ui
Scenario: Iniciar sesión en la aplicación

Given driver 'https://example.com/login'
And input '#username' 'usuarioprueba'
And input '#password' 'password123'
And click 'button[type="submit"]'
And wait 2
Then match text 'h1' == 'Bienvenido'
```

### Pruebas Data-Driven

**data.csv:**

```csv
username,password
user1,pass1
user2,pass2
```

**test.feature:**

```gherkin
Data source: data.csv

Scenario: Iniciar sesión con múltiples usuarios
Given url 'https://api.example.com/login'
And request { "username": "#(username)", "password": "#(password)" }
When method post
Then status 200
```

---

## 🎯 Comandos Soportados

### Pruebas de API

| Comando       | Descripción              | Ejemplo                                     |
| ------------- | ------------------------ | ------------------------------------------- |
| `Given url`   | Establecer URL base      | `Given url 'https://api.example.com'`       |
| `And path`    | Agregar path a la URL    | `And path 'users/1'`                        |
| `And header`  | Establecer header        | `And header Authorization = 'Bearer token'` |
| `And request` | Establecer cuerpo        | `And request { "name": "John" }`            |
| `When method` | Ejecutar método HTTP     | `When method post`                          |
| `Then status` | Validar código de estado | `Then status 200`                           |
| `And match`   | Validar campo respuesta  | `And match response.name == 'John'`         |

### Pruebas de UI

| Comando           | Descripción         | Ejemplo                              |
| ----------------- | ------------------- | ------------------------------------ |
| `Given driver`    | Abrir navegador     | `Given driver 'https://example.com'` |
| `And input`       | Llenar campo        | `And input '#username' 'testuser'`   |
| `And click`       | Hacer clic elemento | `And click 'button.submit'`          |
| `And wait`        | Esperar segundos    | `And wait 3`                         |
| `Then match text` | Validar texto       | `Then match text 'h1' == 'Welcome'`  |

### Fuzzy Matchers

| Matcher    | Descripción         | Ejemplo                                   |
| ---------- | ------------------- | ----------------------------------------- |
| `#notnull` | Valor no es nulo    | `And match response.id == #notnull`       |
| `#null`    | Valor es nulo       | `And match response.deleted == #null`     |
| `#string`  | Valor es un string  | `And match response.name == #string`      |
| `#number`  | Valor es un número  | `And match response.age == #number`       |
| `#boolean` | Valor es un boolean | `And match response.active == #boolean`   |
| `#array`   | Valor es un array   | `And match response.items == #array`      |
| `#object`  | Valor es un objeto  | `And match response.user == #object`      |
| `#uuid`    | Valor es un UUID    | `And match response.id == #uuid`          |
| `#ignore`  | Saltar validación   | `And match response.timestamp == #ignore` |

---

## 🔧 Comandos CLI

```bash
# Inicializar nuevo proyecto
pyrate init

# Ejecutar un archivo feature
pyrate run tests/features/login.feature

# Ejecutar todos los features en una carpeta
pyrate run tests/features/

# Ejecutar con filtrado por tags
pyrate run tests/features/ -t @smoke

# Mostrar versión
pyrate -v
```

---

## 📊 Comparación con Karate Framework

| Característica        | Karate | PyRate | Estado      |
| --------------------- | ------ | ------ | ----------- |
| Sintaxis Gherkin      | ✅     | ✅     | ✅          |
| Pruebas de API        | ✅     | ✅     | ✅          |
| Pruebas de UI         | ✅     | ✅     | ✅          |
| Data-Driven           | ✅     | ✅     | ✅          |
| Fuzzy Matchers        | ✅     | ✅     | ✅          |
| Reportes HTML         | ✅     | ✅     | ✅          |
| Evidencias DOCX       | ❌     | ✅     | **¡Único!** |
| Configuración YAML    | ✅     | ✅     | ✅          |
| Ejecución en Paralelo | ✅     | 🚧     | Roadmap     |

---

## 🛣️ Hoja de Ruta

- [x] **v1.0**: Sistema de configuración con YAML ✅
- [ ] **v1.2**: Ejecución de escenarios en paralelo
- [ ] **v1.3**: Validación de JSON Schema
- [ ] **v1.4**: Soporte para mock server
- [ ] **v2.0**: Soporte para GraphQL

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor siéntete libre de enviar un Pull Request.

1. Haz fork del repositorio
2. Crea tu rama de feature (`git checkout -b feature/CaracteristicaIncreible`)
3. Haz commit de tus cambios (`git commit -m 'Agregar alguna CaracteristicaIncreible'`)
4. Haz push a la rama (`git push origin feature/CaracteristicaIncreible`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- Inspirado en [Karate Framework](https://github.com/karatelabs/karate)
- Construido con [Playwright](https://playwright.dev/) para automatización UI
- Impulsado por [Requests](https://requests.readthedocs.io/) para pruebas de API

---

## 📧 Contacto

- **Autor**: Tu Nombre
- **Email**: tu.email@example.com
- **GitHub**: [@tuusuario](https://github.com/tuusuario)

---

**Hecho con ❤️ para la comunidad de testing**

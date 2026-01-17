# 🚀 PyRate Framework - Guía de Despliegue a PyPI Producción

## ✅ FASE 1 COMPLETADA: Preparación de Archivos

### 📝 Cambios Realizados (v1.0.2)

#### 1️⃣ **Archivos Creados**

- ✅ `pyrate/__main__.py` - Entry point para `python -m pyrate`
- ✅ `MANIFEST.in` - Configuración de empaquetado
- ✅ `.github/workflows/publish.yml` - Workflow de publicación automática

#### 2️⃣ **Archivos Actualizados**

| Archivo              | Cambios Realizados                                                                 |
| -------------------- | ---------------------------------------------------------------------------------- |
| `setup.py`           | ✅ Versión → 1.0.2<br>✅ URL corregida                                             |
| `pyrate/__init__.py` | ✅ Versión → 1.0.2<br>✅ Autor actualizado<br>✅ URL documentación corregida       |
| `pyrate/cli.py`      | ✅ Versión → 1.0.2<br>✅ Fix argparse para `--version`<br>✅ Help message mejorado |
| `README.md`          | ✅ Badges PyPI agregados<br>✅ Contacto actualizado                                |
| `README_ES.md`       | ✅ Badges PyPI agregados<br>✅ Contacto actualizado                                |
| `CHANGELOG.md`       | ✅ Release notes v1.0.2                                                            |

### ✅ Verificación Local

```bash
# ✅ Verificado: python -m pyrate -v
# Resultado: PyRate Framework 1.0.2

# ✅ Verificado: import pyrate
# Version: 1.0.2
# Author: Rafael Enrique Alvarado García
```

---

## 🔄 FASE 2: Git & GitHub Release

### Paso 1: Commit y Push

```bash
# Navegar al proyecto
cd C:\Users\magom\OneDrive\Desktop\fastApi\PyRateProject

# Ver cambios
git status

# Agregar todos los archivos modificados
git add .

# Commit con mensaje descriptivo
git commit -m "chore: release v1.0.2 - CLI fixes and PyPI production prep

- Added __main__.py for python -m pyrate support
- Fixed CLI argument parsing for --version flag
- Corrected repository URLs and metadata
- Created MANIFEST.in for proper package distribution
- Added GitHub Actions workflow for automated PyPI publishing
- Updated documentation with PyPI badges and contact info"

# Push a develop (rama actual)
git push origin develop
```

### Paso 2: Merge a Main

```bash
# Cambiar a main
git checkout main

# Actualizar main
git pull origin main

# Merge develop → main
git merge develop

# Push main
git push origin main
```

### Paso 3: Crear Tag

```bash
# Crear tag anotado
git tag -a v1.0.2 -m "Release v1.0.2 - CLI Fixes and Production Ready

🔧 Fixed:
- CLI entry point with __main__.py
- Argument parsing for --version
- Repository URLs and metadata

📦 Package:
- MANIFEST.in for proper distribution
- GitHub Actions automated publishing

📚 Docs:
- PyPI badges
- Updated contact information"

# Push tag a GitHub
git push origin v1.0.2
```

### Paso 4: Crear GitHub Release (Manual en UI)

1. Ir a: https://github.com/rockefeller2021/PyRateFrameworkTest/releases/new
2. **Tag**: Seleccionar `v1.0.2`
3. **Title**: `v1.0.2 - CLI Fixes & Production Ready`
4. **Description**: Copiar release notes del CHANGELOG.md
5. **✅ Set as latest release**
6. Click **Publish release**

---

## 🏗️ FASE 3: Publicación en PyPI

### Paso 1: Limpiar y Reconstruir

```bash
# Limpiar builds anteriores
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Instalar/actualizar herramientas de build
pip install --upgrade build twine

# Construir paquete
python -m build

# Verificar que se crearon los archivos
dir dist\
# Debe mostrar:
# pyrate_framework-1.0.2-py3-none-any.whl
# pyrate_framework-1.0.2.tar.gz
```

### Paso 2: Verificar Integridad del Paquete

```bash
# Verificar con twine
twine check dist/*

# Resultado esperado:
# Checking dist\pyrate_framework-1.0.2-py3-none-any.whl: PASSED
# Checking dist\pyrate_framework-1.0.2.tar.gz: PASSED
```

### Paso 3: Publicar en TestPyPI (Validación Final)

```bash
# Subir a TestPyPI
twine upload --repository testpypi dist/*

# Cuando pida credenciales:
# Username: __token__
# Password: [Tu API token de TestPyPI]
```

### Paso 4: Verificar Instalación desde TestPyPI

```bash
# En un directorio diferente (ej: PythonProject)
cd C:\Users\magom\OneDrive\Desktop\fastApi\PythonProject

# Crear entorno virtual limpio
python -m venv test_env
test_env\Scripts\activate

# Instalar desde TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pyrate-framework

# ✅ VERIFICACIONES CRÍTICAS:
python -m pyrate -v
# Debe mostrar: PyRate Framework 1.0.2

python -c "import pyrate; print(pyrate.__version__)"
# Debe mostrar: 1.0.2

# Verificar que __main__.py está incluido
python -m pyrate
# Debe mostrar el help

# Limpiar
deactivate
Remove-Item -Recurse test_env
```

### Paso 5: Publicar en PyPI PRODUCCIÓN 🎯

```bash
# IMPORTANTE: Asegúrate de estar en PyRateProject
cd C:\Users\magom\OneDrive\Desktop\fastApi\PyRateProject

# Publicar en PyPI oficial
twine upload dist/*

# Cuando pida credenciales:
# Username: __token__
# Password: [Tu API token de PyPI PRODUCCIÓN]
```

**🔑 Generar API Token de PyPI:**

1. Ir a: https://pypi.org/manage/account/token/
2. Click **"Add API token"**
3. **Token name**: `PyRate-Framework-Upload`
4. **Scope**: `Project: pyrate-framework`
5. **Copiar el token** (empieza con `pypi-`)
6. Usarlo como password en twine

### Paso 6: Verificación Final en PyPI

```bash
# Crear entorno limpio
python -m venv final_test
final_test\Scripts\activate

# Instalar desde PyPI OFICIAL
pip install pyrate-framework

# Verificar versión
python -m pyrate -v
# Debe mostrar: PyRate Framework 1.0.2

# Verificar importación
python -c "from pyrate import PyRateRunner; print('✅ Import successful')"

# Verificar metadata
pip show pyrate-framework

# Limpiar
deactivate
Remove-Item -Recurse final_test
```

---

## 🔐 FASE 4: Configurar Trusted Publishers (Futuro)

Para releases automáticos sin API tokens:

### Paso 1: Configurar en PyPI

1. Ir a: https://pypi.org/manage/account/publishing/
2. Click **"Add a new publisher"**
3. Configurar:
   - **Owner**: `rockefeller2021`
   - **Repository**: `PyRateFrameworkTest`
   - **Workflow**: `publish.yml`
   - **Environment**: (dejar vacío)
4. Click **"Add"**

### Paso 2: Usar Workflow Automatizado

Una vez configurado Trusted Publisher, los releases futuros serán automáticos:

```bash
# Crear release en GitHub (manual o CLI)
gh release create v1.0.3 --title "v1.0.3" --notes "Release notes"

# El workflow .github/workflows/publish.yml se ejecutará automáticamente
# y publicará en PyPI sin credenciales manuales
```

---

## 📊 Checklist Completo

### ✅ Preparación (COMPLETADO)

- [x] Crear `__main__.py`
- [x] Actualizar versión a 1.0.2
- [x] Corregir URLs y metadata
- [x] Crear `MANIFEST.in`
- [x] Agregar badges PyPI
- [x] Crear workflow `publish.yml`
- [x] Actualizar CHANGELOG

### ⏳ Git & Release (SIGUIENTE)

- [ ] Commit cambios
- [ ] Push a develop
- [ ] Merge develop → main
- [ ] Crear tag v1.0.2
- [ ] Crear GitHub Release

### ⏳ Publicación (DESPUÉS)

- [ ] Limpiar builds
- [ ] Reconstruir paquete
- [ ] Verificar con twine
- [ ] Publicar en TestPyPI
- [ ] Verificar instalación TestPyPI
- [ ] Publicar en PyPI PRODUCCIÓN
- [ ] Verificar instalación PyPI

### ⏳ Post-Publicación (OPCIONAL)

- [ ] Configurar Trusted Publishers
- [ ] Anunciar en redes sociales
- [ ] Crear documentación en ReadTheDocs
- [ ] Agregar al README principal del perfil

---

## 🛟 Troubleshooting

### Problema: `pyrate` no se reconoce en PATH

**Solución inmediata**:

```bash
python -m pyrate [comandos]  # Funciona siempre
```

**Solución permanente (Windows)**:

```powershell
# Agregar Scripts al PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$scriptsPath = "C:\Users\magom\AppData\Roaming\Python\Python313\Scripts"
[Environment]::SetEnvironmentVariable("Path", "$userPath;$scriptsPath", "User")

# Reiniciar PowerShell
```

### Problema: Error 403 al subir a PyPI

**Causas posibles**:

1. ❌ Versión ya existe en PyPI
2. ❌ API token incorrecto
3. ❌ API token sin permisos

**Solución**:

- Incrementar versión antes de republicar
- Regenerar API token en PyPI
- Verificar scope del token

### Problema: Archivos faltantes en el paquete

**Verificar**:

```bash
# Extraer el .tar.gz y ver contenido
tar -tzf dist\pyrate_framework-1.0.2.tar.gz

# Debe incluir:
# - README.md
# - LICENSE
# - pyrate/__main__.py
```

**Solución**:

- Verificar `MANIFEST.in`
- Reconstruir con `python -m build --clean`

---

## 🎉 ¡Felicitaciones!

Una vez completadas todas las fases, tu paquete estará:

- ✅ Publicado en PyPI
- ✅ Disponible globalmente: `pip install pyrate-framework`
- ✅ Con metadata profesional
- ✅ Listo para CI/CD automatizado

**URL del paquete**: https://pypi.org/project/pyrate-framework/

---

**Autor**: Rafael Enrique Alvarado García  
**Fecha**: 2026-01-14  
**Versión del paquete**: 1.0.2

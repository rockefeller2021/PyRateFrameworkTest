# 🎥 PyRate Framework - Script Detallado Demo en Vivo

> **Duración Total**: 2 minutos  
> **Objetivo**: Demostrar la simplicidad de PyRate escribiendo y ejecutando un test en vivo

---

## 🎯 **Objetivo del Demo**

Mostrar que con **5 líneas de Gherkin** puedes crear un test completo que:

1. Valida una API REST
2. Automatiza un login en navegador
3. Genera evidencias automáticas
4. Crea reporte HTML profesional

**Sin escribir UNA sola línea de código Python**

---

## 🔧 **Setup Pre-Demo (ANTES de presentar)**

### Preparación del Ambiente (15 min antes)

**Terminal 1 (PowerShell):**

```powershell
# Navegar al proyecto
cd C:\Users\magom\OneDrive\Desktop\fastApi\PyRateProject

# Activar virtual environment
.venv\Scripts\Activate.ps1

# Verificar que PyRate está instalado
python -m pyrate -v
# Output esperado: PyRate Framework 1.0.2
```

**VSCode:**

```
1. Abrir carpeta: PyRateProject
2. Crear archivo: demo.feature (VACÍO)
3. Zoom al 150% para que audiencia vea bien
4. Theme: Dark+ (para contraste)
5. Cerrar todos los demás archivos
```

**Browser (Chrome/Edge):**

```
Tabs preparados (NO cerrar):
1. https://jsonplaceholder.typicode.com/users/1
2. https://www.saucedemo.com
3. http://localhost:8000/reports/ultimo_reporte.html (cerrado por ahora)
```

**Carpetas Limpias:**

```powershell
# Limpiar ejecuciones previas
rm -rf evidence/*
rm -rf reports/*
```

---

## ⏱️ **Timeline del Demo (2 minutos)**

### **Minuto 1: Escribir el Test** (0:00 - 1:00)

#### Segundo 0-10: Introducción

**Narración:**

> "Voy a escribir un test que valida la API de JSONPlaceholder **Y** hace login en SauceDemo. Todo en el mismo archivo, sin código Python."

**Acción:**

- Mostrar VSCode con `demo.feature` vacío
- Manos sobre el teclado (ready to type)

---

#### Segundo 10-30: Test API

**Narración mientras tecleas:**

> "Línea 1: Tag para identificar el test"

**Escribir:**

```gherkin
# @demo @api
```

**Narración:**

> "Línea 2: URL base de la API"

**Escribir:**

```gherkin
Given url 'https://jsonplaceholder.typicode.com'
```

**Narración:**

> "Línea 3: Endpoint que quiero probar"

**Escribir:**

```gherkin
And path 'users/1'
```

**Narración:**

> "Línea 4: Método HTTP GET"

**Escribir:**

```gherkin
When method get
```

**Narración:**

> "Línea 5: Valido que retorne 200 OK"

**Escribir:**

```gherkin
Then status 200
```

**Narración:**

> "Línea 6: Uso un fuzzy matcher para validar que el nombre sea un string, sin importar el valor exacto"

**Escribir:**

```gherkin
And match response.name == #string
```

**Narración:**

> "Línea 7: Valido que el ID no sea nulo"

**Escribir:**

```gherkin
And match response.id == #notnull
```

---

#### Segundo 30-60: Test UI

**Narración:**

> "Ahora UI testing en el mismo archivo. Línea 9: Nuevo tag"

**Escribir:**

```gherkin

# @demo @ui
```

**Narración:**

> "Línea 10: Abro el navegador en SauceDemo"

**Escribir:**

```gherkin
Given driver 'https://www.saucedemo.com'
```

**Narración:**

> "Líneas 11-12: Lleno el formulario de login"

**Escribir:**

```gherkin
And input '#user-name' 'standard_user'
And input '#password' 'secret_sauce'
```

**Narración:**

> "Línea 13: Hago clic en login"

**Escribir:**

```gherkin
And click '#login-button'
```

**Narración:**

> "Línea 14: Espero 2 segundos para que cargue"

**Escribir:**

```gherkin
And wait 2
```

**Narración:**

> "Línea 15: Valido que aparezca 'Products'"

**Escribir:**

```gherkin
Then match text '.title' == 'Products'
```

**Pausa dramática (2 segundos):**

> "Y eso es todo. **15 líneas de Gherkin**. Cero código Python."

---

### **Minuto 2: Ejecutar y Mostrar Resultados** (1:00 - 2:00)

#### Segundo 60-70: Guardar y Ejecutar

**Narración:**

> "Ahora lo ejecuto con un solo comando"

**Acción:**

1. Guardar archivo (Ctrl+S)
2. Cambiar a terminal
3. Mostrar comando ANTES de ejecutar

**Escribir en terminal:**

```powershell
pyrate run demo.feature -t @demo
```

**Narración:**

> "Presiono Enter y PyRate hace su magia"

**Acción:**

- Presionar Enter
- Dejar que corra (3-5 segundos)

---

#### Segundo 70-90: Mostrar Output

**Output esperado en terminal:**

```
[INFO] Ejecutando: demo.feature
[INFO] Escenario: @demo @api
  ✅ Given url 'https://jsonplaceholder.typicode.com'
  ✅ And path 'users/1'
  ✅ When method get
  ✅ Then status 200
  ✅ And match response.name == #string
  ✅ And match response.id == #notnull

[INFO] Escenario: @demo @ui
  ✅ Given driver 'https://www.saucedemo.com'
  ✅ And input '#user-name' 'standard_user'
  ✅ And input '#password' 'secret_sauce'
  ✅ And click '#login-button'
  ✅ And wait 2
  ✅ Then match text '.title' == 'Products'

[SUCCESS] 2/2 escenarios pasaron
[INFO] Evidencia generada: evidence/API_demo_api_Iter1.txt
[INFO] Evidencia generada: evidence/UI_demo_ui_Iter1.docx
[INFO] Reporte HTML: reports/ultimo_reporte.html
```

**Narración:**

> "Como ven, **2 de 2 tests pasaron**. PyRate automáticamente generó:"

**Señalar en terminal:**

> "1. Evidencia de API en formato TXT"
> "2. Evidencia de UI en DOCX con screenshots"
> "3. Reporte HTML profesional"

---

#### Segundo 90-110: Mostrar Evidencia DOCX

**Acción:**

1. Abrir explorador de archivos
2. Navegar a `/evidence/`
3. Abrir `UI_demo_ui_Iter1.docx`

**Narración:**

> "Aquí está la evidencia Word con screenshots automáticos"

**Mostrar (scroll rápido):**

- Título del test
- Timestamp
- Cada paso con status PASS
- Screenshot embebido del browser en SauceDemo

**Narración:**

> "Todo esto generado automáticamente. Cero código extra."

---

#### Segundo 110-120: Mostrar Reporte HTML

**Acción:**

1. Cambiar al browser
2. Ir a tab `http://localhost:8000/reports/ultimo_reporte.html`
3. Si no está abierto, abrir archivo desde explorador

**Narración:**

> "Y finalmente el reporte HTML interactivo"

**Mostrar (scroll rápido):**

- Dashboard con métricas (2/2 PASS)
- Gráfico de pastel verde
- Timeline de ejecución
- Links a evidencias

**Pausa final:**

> "Eso fue PyRate. **De cero a reportes profesionales en 2 minutos**."

---

## 🎬 **Transición de Vuelta a Slides**

**Narración:**

> "Volvamos a la presentación para ver el roadmap"

**Acción:**

- Alt+Tab de vuelta a la presentación
- Continuar con Slide 9 (Roadmap)

---

## 🆘 **Plan B: Si Algo Falla**

### Escenario 1: Internet se cae

**Acción:**

- Mostrar screenshot pre-grabado del demo
- Narración: "Tengo un backup del demo. Como ven aquí..."

**Screenshot debe mostrar:**

- Terminal con output exitoso
- DOCX abierto con screenshot
- HTML report abierto

---

### Escenario 2: Browser no abre en Playwright

**Acción:**

- Comentar rápidamente el test UI
- Solo ejecutar el test API
- Narración: "Por tiempo, voy a ejecutar solo el test API, pero el UI funciona igual"

**Modificar archivo a:**

```gherkin
# @demo @api
Given url 'https://jsonplaceholder.typicode.com'
And path 'users/1'
When method get
Then status 200
And match response.name == #string
And match response.id == #notnull
```

---

### Escenario 3: Terminal se congela

**Acción:**

- Ctrl+C para cancelar
- Narración: "Déjenme cancelar esto y mostrarles un reporte pre-generado"
- Abrir archivo HTML de backup

---

## 📝 **Archivo demo.feature Completo**

**Guardar esto en tu proyecto como backup:**

```gherkin
# @demo @api
Given url 'https://jsonplaceholder.typicode.com'
And path 'users/1'
When method get
Then status 200
And match response.name == #string
And match response.id == #notnull

# @demo @ui
Given driver 'https://www.saucedemo.com'
And input '#user-name' 'standard_user'
And input '#password' 'secret_sauce'
And click '#login-button'
And wait 2
Then match text '.title' == 'Products'
```

---

## 🎯 **Puntos Clave a Mencionar**

### Durante el Demo:

1. **"Cero código Python"** (repetir 2-3 veces)
2. **"15 líneas vs 100+ con pytest"**
3. **"Evidencias automáticas"**
4. **"API + UI en un solo archivo"**

### Después del Demo:

1. **"Esto está en PyPI ahora"**

   ```
   pip install pyrate-framework
   ```

2. **"Open source en GitHub"**

   ```
   github.com/rockefeller2021/PyRateFrameworkTest
   ```

3. **"Listo para producción"**
   - 63 tests unitarios
   - CI/CD con GitHub Actions
   - Python 3.8-3.12

---

## 🎤 **Tips de Presentación del Demo**

### Antes de Empezar:

✅ Respirar profundo
✅ Verificar que terminal está en la carpeta correcta
✅ Verificar que archivo demo.feature existe (aunque vacío)
✅ Zoom al 150% en VSCode

### Durante:

✅ Hablar MIENTRAS tecleas (no silencio incómodo)
✅ Si te equivocas typing → reírte y corregir
✅ Mantener energía alta (esto es emocionante!)
✅ Pausas dramáticas después de ejecutar comando

### Después:

✅ No correr a través de los resultados → darles tiempo de ver
✅ Señalar con el mouse las partes importantes
✅ Sonreír al mostrar el reporte HTML (orgullo)

---

## ⏰ **Comandos de Preparación (Día Anterior)**

```powershell
# 1. Instalar dependencias
pip install pyrate-framework
playwright install chromium

# 2. Crear archivo de demo
New-Item -Path "demo.feature" -ItemType File

# 3. Testear que funciona (práctica)
# (Escribir el test completo)
pyrate run demo.feature -t @demo

# 4. Limpiar para el día del demo
rm -rf evidence/*
rm -rf reports/*

# 5. Pre-grabar screenshot de backup
# Ejecutar demo → Capturar pantalla → Guardar en /backup/
```

---

## 🎬 **Checklist Final Pre-Demo**

**5 Minutos Antes:**

- [ ] Terminal abierto en carpeta correcta
- [ ] VSCode abierto con demo.feature vacío
- [ ] Browser con tabs preparados
- [ ] Evidencias/reportes limpios
- [ ] Screenshot de backup listo
- [ ] Respiración profunda 3x

**Durante Demo:**

- [ ] Hablar mientras tecleas
- [ ] Pausar después de ejecutar
- [ ] Mostrar evidencias con orgullo
- [ ] Sonreír (esto es genial!)

**Después Demo:**

- [ ] Transición suave a slides
- [ ] Mencionar GitHub/PyPI
- [ ] Continuar con energía

---

**Demo Script completo - ¡A practicar! 🚀**

**Tiempo de práctica recomendado:** 5-10 ensayos hasta que salga natural

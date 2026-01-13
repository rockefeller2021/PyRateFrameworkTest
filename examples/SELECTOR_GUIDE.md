# 🎯 Guía Completa de Selectores en PyRate

Este documento muestra todos los tipos de selectores que puedes usar en PyRate con ejemplos prácticos.

---

## 📋 Tipos de Selectores Soportados

### 1️⃣ Selector por ID (`#`)

**Más recomendado** - Es único en la página y muy estable.

```gherkin
# Sintaxis
And input '#id-del-elemento' 'valor'

# Ejemplos reales (SauceDemo)
And input '#user-name' 'standard_user'
And input '#password' 'secret_sauce'
And click '#login-button'
```

**Cuándo usar**: Siempre que el elemento tenga un ID único.

---

### 2️⃣ Selector por Clase (`.`)

Útil para elementos con clases CSS específicas.

```gherkin
# Sintaxis
And click '.nombre-clase'

# Ejemplos reales (SauceDemo)
Then match text '.title' == 'Products'
And click '.shopping_cart_link'
Then match text '.complete-header' == 'Thank you for your order!'
```

**⚠️ Precaución**: Las clases pueden repetirse. Asegúrate que sea única o usa selectores más específicos.

---

### 3️⃣ Selector por Atributo `data-test` / `data-testid`

**Best Practice** - Atributos específicos para testing.

```gherkin
# Sintaxis
And click '[data-test="nombre-test"]'
And click '[data-testid="otro-nombre"]'

# Ejemplos reales (SauceDemo)
And click '[data-test="add-to-cart-sauce-labs-backpack"]'
And click '[data-test="add-to-cart-sauce-labs-bike-light"]'
And click '[data-test="remove-sauce-labs-backpack"]'
```

**Por qué es mejor**:

- No depende de estilos CSS
- Semánticamente indica "esto es para testing"
- Los developers no los cambian sin avisar

---

### 4️⃣ Selector por Atributo Genérico

Cualquier atributo HTML.

```gherkin
# Por nombre
And input '[name="email"]' 'test@example.com'

# Por placeholder
And input '[placeholder="Enter password"]' 'secret123'

# Por type
And click '[type="submit"]'

# Por href
And click '[href="/logout"]'
```

**Ejemplo real (formulario genérico)**:

```gherkin
And input '[name="firstName"]' 'John'
And input '[name="lastName"]' 'Doe'
And input '[name="email"]' 'john@test.com'
And click '[type="submit"]'
```

---

### 5️⃣ Selectores Combinados (CSS complejo)

Combina múltiples selectores para mayor precisión.

```gherkin
# Descendiente directo (>)
And click 'div.cart > button.checkout'

# Primer hijo
Then match text '.cart_item:first-child .inventory_item_name' == 'Product Name'

# Último hijo
And click 'ul.menu li:last-child a'

# Por posición
And click 'tr:nth-child(2) td button'

# Combinación de clase + atributo
And click 'button.primary[type="submit"]'
```

**Ejemplo real (SauceDemo - tabla de productos)**:

```gherkin
# Seleccionar el primer producto de la lista
And click '.inventory_item:first-child .btn_inventory'

# Verificar nombre del segundo producto
Then match text '.inventory_item:nth-child(2) .inventory_item_name' == 'Sauce Labs Bike Light'
```

---

### 6️⃣ Selector por Tipo de Elemento

Elementos HTML directos.

```gherkin
# Elementos HTML
And click 'button'
And input 'input'
Then match text 'h1' == 'Welcome'

# Con especificidad
And click 'form button[type="submit"]'
And input 'form#loginForm input[name="username"]' 'admin'
```

---

### 7️⃣ Selector por Texto (Playwright)

Busca elementos por su texto visible.

```gherkin
# Texto exacto
And click 'text=Login'
And click 'text=Add to Cart'

# Texto parcial (contiene)
And click 'text=Continue Shopping'
Then match text 'text=Thank you' == #string
```

**Ejemplo real**:

```gherkin
And click 'text=Add to cart'
And click 'text=Checkout'
Then match text 'text=Thank you for your order!' == 'Thank you for your order!'
```

---

### 8️⃣ Selector XPath

Xpath para casos muy específicos.

```gherkin
# XPath absoluto (evitar)
And click '//div[@id="root"]/div/div/button'

# XPath relativo (mejor)
And click '//button[@type="submit"]'
And input '//input[@placeholder="Username"]' 'testuser'

# XPath con texto
And click '//button[contains(text(), "Add to Cart")]'
```

**Recomendación**: Usa CSS siempre que sea posible, XPath solo cuando CSS no funciona.

---

## 🎯 Ejemplos del Mundo Real

### Ejemplo Completo: SauceDemo E-commerce

Ver archivo: [`saucedemo_selectors.feature`](saucedemo_selectors.feature)

```gherkin
# Login con selectores por ID
And input '#user-name' 'standard_user'
And input '#password' 'secret_sauce'
And click '#login-button'

# Agregar producto con data-test
And click '[data-test="add-to-cart-sauce-labs-backpack"]'

# Ir al carrito con clase CSS
And click '.shopping_cart_link'

# Verificar producto con selector combinado
Then match text '.cart_item:first-child .inventory_item_name' == 'Sauce Labs Backpack'
```

---

### Ejemplo: Formulario de Contacto

```gherkin
Scenario: Enviar formulario de contacto

Given driver 'https://example.com/contact'

# Selectores por name (común en formularios)
And input '[name="fullName"]' 'John Doe'
And input '[name="email"]' 'john@example.com'
And input '[name="phone"]' '+1234567890'

# Textarea con ID
And input '#message' 'Este es mi mensaje de prueba'

# Checkbox con atributo
And click '[type="checkbox"][name="acceptTerms"]'

# Submit con clase CSS
And click 'button.submit-form'

# Verificar mensaje de éxito con clase
Then match text '.success-message' == 'Message sent successfully!'
```

---

### Ejemplo: Tabla Dinámica

```gherkin
Scenario: Interactuar con tabla de datos

Given driver 'https://example.com/users'

# Hacer clic en la segunda fila, columna de acciones
And click 'tr:nth-child(2) .actions-column button.edit'

# Verificar datos de la primera fila
Then match text 'tbody tr:first-child td:nth-child(2)' == 'John Doe'

# Ordenar por columna (clic en header)
And click 'thead th:nth-child(3)'
```

---

## 💡 Mejores Prácticas

### ✅ **Orden de Preferencia**:

1. **`data-testid` / `data-test`** → Más estable

   ```gherkin
   And click '[data-testid="submit-button"]'
   ```

2. **ID único** → Muy estable

   ```gherkin
   And click '#login-submit'
   ```

3. **Atributos semánticos** → Bastante estable

   ```gherkin
   And click '[aria-label="Close modal"]'
   And click '[role="button"]'
   ```

4. **Clases CSS** → Usar con cuidado

   ```gherkin
   And click '.btn-primary'
   ```

5. **Texto visible** → Puede cambiar con traducciones
   ```gherkin
   And click 'text=Login'
   ```

### ❌ **Evitar**:

- ❌ Selectores muy largos: `.container > div > div > div > button`
- ❌ Basados en posición sin contexto: `div:nth-child(5)`
- ❌ XPath absoluto: `//html/body/div[1]/div[2]/button`
- ❌ Clases de estilos dinámicos: `.css-1x2y3z4`

---

## 🔍 Cómo Encontrar Selectores

### Opción 1: DevTools del Navegador

1. F12 → Inspector
2. Clic derecho en elemento → Inspeccionar
3. Clic derecho en HTML → Copy → Copy Selector

### Opción 2: Playwright Inspector

```bash
playwright codegen https://www.saucedemo.com
```

Esto abrirá un inspector que genera selectores automáticamente mientras interactúas.

### Opción 3: Consola del Navegador

```javascript
// Probar selector en consola
document.querySelector("#user-name");
document.querySelectorAll(".inventory_item");
```

---

## 📚 Recursos Adicionales

- [Selectores CSS - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [Playwright Selectors](https://playwright.dev/docs/selectors)
- [Práctica con SauceDemo](https://www.saucedemo.com)

---

**Creado por**: PyRate Framework  
**Última actualización**: 2026-01-11

# @ui @xpath
# Ejemplo de uso de selectores XPath en PyRate v1.1.0

Scenario: Login usando XPath selectors

# Navego a SauceDemo
Given driver 'https://www.saucedemo.com'

# ===== CSS SELECTORS (Retrocompatibles) =====

# Ingreso usuario con CSS (funciona igual que v1.0.2)
And input '#user-name' 'standard_user'

# Ingreso password con CSS
And input '#password' 'secret_sauce'

# Click con CSS
And click '#login-button'

# Espero carga
And wait 2

# Valido con CSS
Then match text '.title' == 'Products'


# ===== XPATH CON PREFIJO =====

Scenario: Login usando XPath con prefijo

Given driver 'https://www.saucedemo.com'

# Con prefijo explícito "xpath="
And input 'xpath=//input[@id="user-name"]' 'standard_user'
And input 'xpath=//input[@id="password"]' 'secret_sauce'
And click 'xpath=//input[@id="login-button"]'
And wait 2
Then match text 'xpath=//span[@class="title"]' == 'Products'


# ===== XPATH AUTO-DETECTADO =====

Scenario: Login usando XPath auto-detectado

Given driver 'https://www.saucedemo.com'

# Auto-detectado (empieza con //)
And input '//input[@id="user-name"]' 'standard_user'
And input '//input[@placeholder="Password"]' 'secret_sauce'

# XPath con atributo de texto
And click '//input[@type="submit" and @value="Login"]'

And wait 2

# XPath con contains
Then match text '//span[contains(@class, "title")]' == 'Products'


# ===== XPATH AVANZADO =====

Scenario: Formularios complejos con XPath

Given driver 'https://example.com/form'

# XPath relativo
And input '//div[@id="form"]/input[@name="username"]' 'admin'

# XPath con texto contiene
And click '//button[contains(text(), "Submit")]'

# XPath con índice
And input '(//input[@type="text"])[1]' 'first-input'

# XPath con parent
And click '//span[@class="label"]/parent::div//button'

# XPath con ancestor
And input '//table[@id="data"]//tr[2]//input' 'row-2-value'


# ===== MEZCLA CSS Y XPATH =====

Scenario: Uso combinado de CSS y XPath

Given driver 'https://www.saucedemo.com'

# Puedo mezclar ambos tipos de selectores libremente
And input '#user-name' 'standard_user'  # CSS
And input '//input[@id="password"]' 'secret_sauce'  # XPath
And click '#login-button'  # CSS
And wait 2
Then match text '//span[@class="title"]' == 'Products'  # XPath


# ===== CASOS REALES DE USO =====

Scenario: Formulario con estructura dinámica

Given driver 'https://example.com/dynamic-form'

# Cuando el ID cambia dinámicamente, XPath es útil
And input '//input[starts-with(@id, "username-")]' 'john'

# Cuando necesitas navegar por jerarquía
And input '//form[@name="login"]//input[@type="password"]' 'pass123'

# Cuando el selector CSS es muy complejo
And click '//button[@data-test-id="submit-btn"]'

# Validación con XPath condicional
Then match text '//div[@role="alert" and contains(@class, "success")]' == 'Login successful'

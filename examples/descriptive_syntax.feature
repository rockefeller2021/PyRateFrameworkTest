# @ui @descriptive
# Ejemplo completo de sintaxis descriptiva en PyRate v1.1.0-beta.2

Scenario: Login exitoso con descripciones legibles

# Navego a la página principal de SauceDemo
Given driver 'https://www.saucedemo.com

'

# Ingreso el nombre de usuario 'standard_user' en el campo de login
And input '#user-name' 'standard_user'

# Ingreso la contraseña secreta en el campo password
And input '#password' 'secret_sauce'

# Hago clic en el botón de iniciar sesión
And click '#login-button'

# Espero 2 segundos para que cargue el dashboard
And wait 2

# Valido que aparece el título 'Products' indicando login exitoso
Then match text '.title' == 'Products'


# ===== EJEMPLO SIN DESCRIPCIONES (Backward Compatible) =====

Scenario: Login simple sin descripciones

Given driver 'https://www.saucedemo.com'
And input '#user-name' 'standard_user'
And input '#password' 'secret_sauce'
And click '#login-button'
And wait 2
Then match text '.title' == 'Products'


# ===== EJEMPLO MIXTO =====

Scenario: Prueba de carrito con descripciones mixtas

# Navego a SauceDemo
Given driver 'https://www.saucedemo.com'

# Completo credenciales de login
And input '#user-name' 'standard_user'
And input '#password' 'secret_sauce'
And click '#login-button'

And wait 2

# Agrego el primer producto al carrito
And click '.inventory_item:first-child .btn_inventory'

# Valido que el badge muestra '1'
Then match text '.shopping_cart_badge' == '1'


# ===== EJEMPLO CON TAGS =====

# @smoke @ui @regression
Scenario: Login con tags y descripciones

# Inicio sesión con usuario estándar
Given driver 'https://www.saucedemo.com'

# @checkpoint
And input '#user-name' 'standard_user'
And input '#password' 'secret_sauce'

# Presiono botón de login
And click '#login-button'

And wait 2

Then match text '.title' == 'Products'

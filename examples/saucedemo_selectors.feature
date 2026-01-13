# @ui @demo @saucedemo
# Ejemplo completo con diferentes tipos de selectores CSS
# Sitio: https://www.saucedemo.com

Scenario: Login y agregar producto al carrito usando diversos selectores

# ========================================
# LOGIN - Usando selectores por ID
# ========================================
Given driver 'https://www.saucedemo.com'

# Selector por ID (más común y recomendado)
And input '#user-name' 'standard_user'
And input '#password' 'secret_sauce'

# Selector por ID del botón
And click '#login-button'
And wait 2

# ========================================
# VERIFICAR LOGIN - Selector por clase CSS
# ========================================
# Verificar que llegamos al inventario (selector por clase)
Then match text '.title' == 'Products'

# ========================================
# AGREGAR PRODUCTO - Selectores por data-testid
# ========================================
# SauceDemo usa data-test como atributo (best practice para testing)

# Agregar "Sauce Labs Backpack" usando data-test
And click '[data-test="add-to-cart-sauce-labs-backpack"]'

# Agregar "Sauce Labs Bike Light" usando data-test
And click '[data-test="add-to-cart-sauce-labs-bike-light"]'

# ========================================
# IR AL CARRITO - Selector por clase CSS
# ========================================
# El badge del carrito usa clase
And click '.shopping_cart_link'
And wait 1

# ========================================
# VERIFICAR CARRITO - Selectores combinados
# ========================================
# Verificar título del carrito (selector por clase)
Then match text '.title' == 'Your Cart'

# Verificar cantidad de items (selector por clase)
Then match text '.cart_quantity' == '2'

# Verificar nombre del primer producto (selector complejo CSS)
Then match text '.cart_item:first-child .inventory_item_name' == 'Sauce Labs Backpack'

# ========================================
# CHECKOUT - Selectores por ID
# ========================================
And click '#checkout'
And wait 1

# Llenar formulario con selectores por ID
And input '#first-name' 'John'
And input '#last-name' 'Doe'
And input '#postal-code' '12345'

# Continuar con selector por ID
And click '#continue'
And wait 1

# ========================================
# VERIFICAR RESUMEN - Selectores por clase
# ========================================
Then match text '.title' == 'Checkout: Overview'

# Verificar total con selector de clase específico
Then match text '.summary_subtotal_label' == #string

# Finalizar compra
And click '#finish'
And wait 2

# ========================================
# VERIFICAR ÉXITO - Selector por clase
# ========================================
Then match text '.complete-header' == 'Thank you for your order!'

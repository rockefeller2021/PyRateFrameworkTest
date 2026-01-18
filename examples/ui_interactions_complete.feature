# PyRate Framework - Complete UI Interactions Example
# This example demonstrates all Sprint 3 UI interaction features

Feature: Complete UI Interactions Demo

Scenario: Scroll Commands Demo
    Given driver 'https://the-internet.herokuapp.com/large'
    
    # Scroll to specific element
    And scroll to element '#content'
    And wait 1
    
    # Scroll to top
    And scroll to top
    And wait 1
    
    # Scroll to bottom
    And scroll to bottom
    And wait 1
    
    # Scroll to coordinates
    And scroll to 0, 500
    And wait 1

Scenario: Dropdown Selection Demo
    Given driver 'https://the-internet.herokuapp.com/dropdown'
    
    # Select by visible text
    And select '#dropdown' by text 'Option 1'
    And wait 1
    
    # Select by value
    And select '#dropdown' by value '2'
    And wait 1
    
    # Select by index
    And select '#dropdown' by index 1
    And wait 1

Scenario: Checkbox Operations Demo
    Given driver 'https://the-internet.herokuapp.com/checkboxes'
    
    # Check checkbox
    And check '//input[@type="checkbox"][1]'
    And wait 1
    
    # Uncheck checkbox
    And uncheck '//input[@type="checkbox"][2]'
    And wait 1
    
    # Toggle checkbox
    And toggle '//input[@type="checkbox"][1]'
    And wait 1
    And toggle '//input[@type="checkbox"][1]'
    And wait 1

Scenario: Radio Button Demo
    Given driver 'https://www.selenium.dev/selenium/web/web-form.html'
    
    # Select radio button
    And check radio '#my-radio-1'
    And wait 1
    
    # Select another radio
    And check radio '#my-radio-2'
    And wait 1

Scenario: Iframe Navigation Demo
    Given driver 'https://the-internet.herokuapp.com/iframe'
    
    # Switch to iframe
    And switch to frame '#mce_0_ifr'
    And wait 1
    
    # Return to main page
    And switch to default content
    And wait 1

Scenario: Alert Handling Demo
    Given driver 'https://the-internet.herokuapp.com/javascript_alerts'
    
    # Accept alert
    And click '//button[text()="Click for JS Alert"]'
    And accept alert
    And wait 1
    
    # Dismiss confirm
    And click '//button[text()="Click for JS Confirm"]'
    And dismiss alert
    And wait 1
    
    # Type in prompt
    And click '//button[text()="Click for JS Prompt"]'
    And type in prompt 'PyRate Framework'
    And wait 1

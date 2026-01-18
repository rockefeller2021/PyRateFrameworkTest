# PyRate Framework - Complete Form Interaction Example
# Demonstrates real-world form handling with all Sprint 3 features
Feature: Complete Form Interaction

  Scenario: User Registration Form
    # Navigate to form
    Given driver 'https://www.selenium.dev/selenium/web/web-form.html'
    And wait 1
    # Text inputs
    And input '#my-text-id' 'John Doe'
    And input '//input[@name="my-password"]' 'SecurePass123'
    And wait 1
    # Textarea
    And input '//textarea[@name="my-textarea"]' 'This is a test message from PyRate Framework'
    And wait 1
    # Dropdown selection
    And select '//select[@name="my-select"]' by text 'Two'
    And wait 1
    # Checkboxes
    And check '#my-check-1'
    And check '#my-check-2'
    And wait 1
    # Radio buttons
    And check radio '#my-radio-1'
    And wait 1
    # Scroll to submit button
    And scroll to element '//button[@type="submit"]'
    And wait 1
    # Submit form
    And click '//button[@type="submit"]'
    And wait 2
    # Verify success message
    Then match text '#message' == 'Received!'

  Scenario: Dynamic Form with Alerts
    Given driver 'https://the-internet.herokuapp.com/javascript_alerts'
    # Interact with alerts
    And click '//button[text()="Click for JS Prompt"]'
    And type in prompt 'Test User'
    And wait 1
    # Verify result
    Then match text '#result' == 'You entered: Test User'

  Scenario: Multi-step Form with Iframes
    Given driver 'https://the-internet.herokuapp.com/iframe'
    # Switch to iframe and interact
    And switch to frame '#mce_0_ifr'
    And wait 1
    # Type in iframe content
    And input '#tinymce' 'Content typed inside iframe'
    And wait 1
    # Return to main page
    And switch to default content
    And wait 1
    # Verify we're back on main page
    Then match text 'h3' == 'An iFrame containing the TinyMCE WYSIWYG Editor'

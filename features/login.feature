Feature: Juice Shop Login

  As a registered user
  I want to login to OWASP Juice Shop
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given the Juice Shop login page is open
    When the user enters valid credentials
    And clicks the login button
    Then the user should be logged in successfully
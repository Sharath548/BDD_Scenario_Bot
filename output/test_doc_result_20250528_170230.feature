 Feature: User Registration

   Scenario: Successful registration of a new user
      Given I am on the registration page
      When I enter a valid name, email, and password
      And I confirm my password
      And I click the "Register" button
      Then I should receive a success message
      And I should be redirected to the login page

   Scenario: Registration failure due to invalid email format
      Given I am on the registration page
      When I enter an invalid email address and valid name and password
      And I confirm my password
      And I click the "Register" button
      Then I should receive an error message about the email format
      And I should remain on the registration page

   Scenario: Registration failure due to already existing user with the same email
      Given I am on the registration page
      And there is a user with the same email address registered in the system
      When I enter that email and valid name and password
      And I confirm my password
      And I click the "Register" button
      Then I should receive an error message about the email already being in use
      And I should remain on the registration page

   Scenario: Registration failure due to empty fields
      Given I am on the registration page
      When I do not enter any information or leave a field empty
      And I click the "Register" button
      Then I should receive an error message about required fields
      And I should remain on the registration page
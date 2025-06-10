calca Feature: User Registration in Online Bookstore

   Scenario: Successful User Registration
      Given I am a new user visiting the Online Bookstore website
      When I navigate to the registration page
      And I enter my Name, Email, and Password
      And I click on the "Register" button
      Then I should receive a confirmation message that my account has been created successfully
      And I should be able to log in using my newly created credentials
      And I should be redirected to my profile page

   Scenario: Invalid Email Format during User Registration
      Given I am a new user visiting the Online Bookstore website
      When I navigate to the registration page
      And I enter an invalid email format (e.g., example)
      And I click on the "Register" button
      Then I should receive an error message indicating that the email format is invalid
      And I should still be on the registration page

   Scenario: Existing Email during User Registration
      Given I am a new user visiting the Online Bookstore website
      When I navigate to the registration page
      And I enter an email address that is already registered
      And I click on the "Register" button
      Then I should receive an error message indicating that the email address is already in use
      And I should still be on the registration page

   Feature: User Login and Logout

   Scenario: Successful User Login
      Given I have registered an account with the Online Bookstore
      When I navigate to the login page
      And I enter my Email and Password
      And I click on the "Login" button
      Then I should be redirected to my profile page
      And I should see a welcome message for my username

   Scenario: Incorrect Credentials during User Login
      Given I have registered an account with the Online Bookstore
      When I navigate to the login page
      And I enter incorrect Email and/or Password
      And I click on the "Login" button
      Then I should receive an error message indicating that the credentials are incorrect
      And I should still be on the login page
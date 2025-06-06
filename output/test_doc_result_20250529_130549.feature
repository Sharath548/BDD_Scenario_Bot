 Feature: User Registration in Online Bookstore

   Scenario: Successful User Registration
      Given I am on the registration page
      When I enter a valid name, email, and password
      And I agree to terms of service
      And click on "Register" button
      Then I should be successfully registered and logged in
      And I should see a confirmation message
      And I should be redirected to my profile page

   Scenario: Invalid Email Format during Registration
      Given I am on the registration page
      When I enter an invalid email format
      And I click on "Register" button
      Then I should receive an error message "Please provide a valid email address"
      And I should stay on the registration page

   Scenario: Existing User Trying to Register
      Given A user is registered with the given email
      When This user tries to register again with the same email
      Then I should receive an error message "Email already in use. Please log in instead."
      And I should stay on the registration page

   Feature: User Login in Online Bookstore

   Scenario: Successful User Login
      Given I am on the login page
      When I enter valid email and password
      And click on "Login" button
      Then I should be successfully logged in
      And I should be redirected to my profile page

   Scenario: Incorrect Credentials during Login
      Given I am on the login page
      When I enter invalid email or password
      And click on "Login" button
      Then I should receive an error message "Invalid Email or Password"
      And I should stay on the login page

   Feature: User Logout in Online Bookstore

   Scenario: Successful User Logout
      Given I am logged in
      When I click on "Logout" button
      Then I should be successfully logged out
      And I should be redirected to the login page
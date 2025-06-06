 Feature: User Registration

   Scenario: Successful User Registration
      Given I am on the registration page
      When I fill in the fields with a valid name, email, and password
      And I click the "Register" button
      Then I should be redirected to the login page
      And I should receive an account confirmation email
      And my account details should be saved in the system

   Scenario: Invalid Email Format
      Given I am on the registration page
      When I fill in the fields with a valid name, password and an invalid email format
      And I click the "Register" button
      Then an error message should be displayed indicating an invalid email format
      And I should remain on the registration page

   Scenario: Empty Fields
      Given I am on the registration page
      When I do not fill in any fields and click the "Register" button
      Then an error message should be displayed for each empty field
      And I should remain on the registration page

   Feature: User Login

   Scenario: Successful User Login
      Given I am on the login page
      When I enter my registered email and password
      And I click the "Login" button
      Then I should be redirected to the dashboard

   Scenario: Incorrect Email or Password
      Given I am on the login page
      When I enter an incorrect email or password
      And I click the "Login" button
      Then an error message should be displayed indicating incorrect credentials
      And I should remain on the login page

   Feature: User Logout

   Scenario: Successful User Logout
      Given I am logged in
      When I click the logout button
      Then I should be redirected to the login page
      And my session should be terminated

   Feature: Profile Update

   Scenario: Successfully updating user profile details
      Given I am logged in
      When I navigate to my profile page and update any field
      And I click the "Save" button
      Then my updated details should be saved in the system
      And I should see a success message
      And my updated details should be reflected on my profile page
 Feature: User Registration

   Scenario: Successful user registration
     Given I am on the registration page
     When I fill in a valid name, email and password
     And I click the 'Register' button
     Then I should be redirected to the login page with success message
     And my account should be created with the provided details

   Scenario: Unsuccessful user registration due to invalid email format
     Given I am on the registration page
     When I fill in an invalid email address and a valid name and password
     And I click the 'Register' button
     Then I should see an error message indicating an invalid email format
     And my account should not be created

   Scenario: Unsuccessful user registration due to existing email address
     Given A user with the provided email already exists
     When I fill in a valid name, that email and password on the registration page
     And I click the 'Register' button
     Then I should see an error message indicating that the email is already registered
     And my account should not be created

   Feature: User Login

   Scenario: Successful user login with valid credentials
     Given I am on the login page
     When I enter a valid email and password
     And I click the 'Login' button
     Then I should be redirected to my profile page

   Scenario: Unsuccessful user login due to invalid credentials
     Given I am on the login page
     When I enter an incorrect email or password
     And I click the 'Login' button
     Then I should see an error message indicating invalid credentials
     And I should remain on the login page

   Feature: User Logout

   Scenario: Successful user logout
     Given I am logged in to my account
     When I click the 'Logout' button
     Then I should be redirected to the login page
     And I should no longer be considered as a logged-in user

   Feature: Profile Update

   Scenario: Successful profile update with valid data
     Given I am logged in to my account
     When I navigate to my profile page and fill in updated name, email, or password
     And I click the 'Update' button
     Then I should see a success message indicating successful update
     And the updated details should be displayed on my profile page

   Scenario: Unsuccessful profile update with empty fields
     Given I am logged in to my account and navigated to my profile page
     When I leave one or more required fields empty and click the 'Update' button
     Then I should see an error message indicating missing information
     And the fields with missing data should be highlighted for correction
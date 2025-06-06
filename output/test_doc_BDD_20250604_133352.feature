 Feature: Verifying the Functionality of The Online Bookstore

   Scenario: User Registration
      Given I am on the registration page of the online bookstore
      When I fill out the required fields (name, email, and password) and submit the form
      Then I should receive a confirmation message that my account has been created successfully
      And I should be able to log in with the provided credentials

   Scenario: Login Process
      Given I am on the login page of the online bookstore
      When I enter my email and password and submit the form
      Then I should be redirected to the dashboard if the credentials are valid
      And If the credentials are invalid, I should see an error message

   Scenario: Logout Process
      Given I am logged in to the online bookstore
      When I navigate to any page and click on the logout button
      Then I should be redirected to the login page and no longer be logged in

   Scenario: Profile Update
      Given I am logged into the online bookstore
      When I navigate to my profile page and update my personal information (name, email, or password)
      Then The changes should be saved, and my updated information should be reflected on my profile page

   Feature: Verifying Book Browsing Functionality

   Scenario: Browse Books by Categories
      Given I am logged into the online bookstore
      When I navigate to the books section of the dashboard
      Then I should see various categories of books (e.g., Fiction, Non-Fiction, Technology, etc.)
      And When I select a category, I should see a list of relevant books

   Scenario: Adding Books to Shopping Cart
      Given I am logged into the online bookstore and browsing books in a specific category
      When I find a book I want to purchase and click on its "Add to Cart" button
      Then The book should be added to my shopping cart

   Scenario: Making Payments via Simulated Gateway
      Given I have added at least one book to my shopping cart
      When I navigate to the checkout page and provide my billing information
      Then I should be able to complete the payment process using the simulated gateway (e.g., by providing a valid credit card number, expiration date, and CVC code)
      And After the payment is processed successfully, I should receive a confirmation message and an email receipt for my purchase

   Feature: Verifying System Notifications in Online Bookstore

   Scenario: Receiving Notification about Purchase Confirmation
      Given I have made a successful purchase in the online bookstore
      When I check my email or the notification center in the system
      Then I should receive a notification confirming my purchase with relevant details (e.g., book title, price, and date of purchase)

   Scenario: Checking the details of a purchase notification
      Given I have received a notification about a successful purchase
      When I tap on the notification to view its details
      Then I should see the relevant information regarding my purchase, including the book title, price, and transaction ID (if any)
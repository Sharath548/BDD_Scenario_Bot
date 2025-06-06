 Feature: Verifying Text Data in the Banking System

   Scenario: Checking Transaction Details
      Given I have the text data related to a transaction
      When I analyze the text data for the transaction number and amount
      Then I should find "HOPAPP0061789" as the transaction number and "1,74,000" as the transaction amount

   Scenario: Checking Currency Conversion Details
      Given I have the text data related to a transaction with an FX rate
      When I analyze the text data for the currency conversion details
      Then I should find the exchange rate between INR and GBP as "113.73"

   Scenario: Verifying Sender's Name
      Given I have the text data related to a transaction
      When I check the name of the sender in the transaction data
      Then I should see "SHARATH CHANDRA REDDY KAKULAVARAM" as the sender's name

   Scenario: Verifying Transaction Type
      Given I have the text data related to a transaction
      When I check the type of the transaction in the displayed text data
      Then I should see "AIC" as the transaction type for this specific case

   Feature: Verifying Functionality of the Online Banking App

   Scenario: Checking Balance
      Given I am logged into the online banking app
      When I navigate to my account balance section
      Then I should see the current account balance displayed on the screen

   Scenario: Transferring Funds
      Given I have sufficient funds in my account and am logged into the online banking app
      When I initiate a fund transfer to another account with specified details (recipient's name, account number, amount, and destination bank)
      Then I should receive a confirmation message that the transfer has been initiated successfully
      And I should see the transaction related to this transfer in my recent transactions list

   Scenario: Setting Up Recurring Payments
      Given I am logged into the online banking app
      When I navigate to the recurring payments section and set up a payment with specified details (amount, frequency, recipient's account number, and destination bank)
      Then The payment should be saved, and it should recur according to the set schedule

   Scenario: Checking Account Activity
      Given I am logged into the online banking app
      When I navigate to my account activity section
      Then I should see a list of recent transactions related to my account

   Feature: Verifying Notifications in Online Banking App

   Scenario: Receiving Notification about Transaction Confirmation
      Given I have made a transaction in the online banking app
      When I check my notifications in the system
      Then I should receive a notification confirming my transaction with relevant details (e.g., amount, recipient's name, and date of transaction)

   Scenario: Checking the details of a transaction notification
      Given I have received a notification about a successful transaction
      When I tap on the notification to view its details
      Then I should see the relevant information regarding my transaction, including the amount, recipient's name, and transaction number (if any)
 Feature: Online Seva Booking for Yadadri Bhuvanagiri Temple

    Scenario: Successful Online Payment for a Seva booking
      Given I have navigated to the official website "<https://yadagiriguttatemple.telangana.gov.in>"
      And I am on the homepage of the Yadagirigutta Temple
      And I am logged in with valid credentials as a registered user
      When I navigate to the "Online Seva Booking" section
      And I select the desired Seva ("Sri Swamy Vari Nitya Kalyanam")
      And I fill out the required details (Name, Mobile, Email, Quantity, Age, etc.)
      And I choose the date and timings for the Seva
      And I agree to the Terms & Conditions
      And I make an online payment using a valid credit/debit card or net banking
      Then I should receive a receipt with the following details:
        | Receipt Number         | generated automatically by the system |
        | Payment mode           | Online Payment                      |
        | Transaction Status    | Success                             |
        | Purpose of Payment    | Online Seva Booking                |
        | Seva Name              | Sri Swamy Vari Nitya Kalyanam      |
        | Seva Date              | selected date                       |
        | Mobile                 | provided mobile number             |
        | Email                  | provided email address            |
        | Quantity               | selected quantity                  |
        | Age                    | provided age                       |
        | Price                  | total price in INR                  |
        | Persons Allowed        | 2 (as per the booking)              |
        | Reporting Time         | 09:00 AM                           |
        | Reporting Place        | Main Entrance of the Temple       |
        | Total Price            | total price in words                |
      And I should receive a confirmation message with the same details
      And I should be able to download or print the receipt
      And I should not be allowed to book the same Seva again without canceling the existing booking

    Scenario: Unsuccessful Online Payment for a Seva booking
      Given I have navigated to the official website "<https://yadagiriguttatemple.telangana.gov.in>"
      And I am on the homepage of the Yadagirigutta Temple
      And I am logged in with valid credentials as a registered user
      When I navigate to the "Online Seva Booking" section
      And I select the desired Seva ("Sri Swamy Vari Nitya Kalyanam")
      And I fill out the required details (Name, Mobile, Email, Quantity, Age, etc.)
      And I choose the date and timings for the Seva
      And I agree to the Terms & Conditions
      And I make an unsuccessful online payment using invalid credit/debit card or net banking details
      Then I should receive an error message indicating the failed transaction
      And I should not be able to proceed with the booking process

    Scenario: Canceling an existing Online Seva booking
      Given I have a confirmed Online Seva booking for Yadagirigutta Temple
      When I navigate to my account dashboard on the official website
      And I find and select the booking I want to cancel
      Then I should be able to initiate the cancellation process
      And I should receive a confirmation message that the booking has been cancelled
      And I should not be charged for the cancelled Seva booking
      And I should not be allowed to rebook the same Seva on the same date and timings without a new booking slot becoming available
 Feature: Verify Certificate of Completion

   Scenario: As a Retail Manager, I want to verify the authenticity of an employee's Certificate of Completion for Macy's Introduction to Enactor Certification Test

   Given I am logged in as a Retail Manager
   And I have access to the Employee Records System
   And there is an employee named "Sharath Chandrareddy" with the record containing "Macys Introduction to Enactor Certification Test"
   When I navigate to the employee's record
   And I check for the issued date and time of the certificate
   Then the date should match "ap 1, 2028"
   And the time should match "217 pm"
   And I should see the issuer's name as "Mike Carrell"
   When I verify the status of the certificate
   Then it should be marked as "Successful Completed"
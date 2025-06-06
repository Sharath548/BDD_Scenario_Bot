 Feature: Verify Certificate of Completion Validation

   Scenario: Validate a valid Certificate of Completion
      Given I am a retail system user
      And I have the following Certificate of Completion text: "Certificate of Completion sharath chandrareddy nas sucessful completed Macys Introduction to Enactor Certification Test ap 1, 2028, 217 pm Mike Carrell"
      When I enter the provided text into the system
      Then the system should return a success message indicating validity

   Scenario: Validate an invalidly formatted Certificate of Completion
      Given I am a retail system user
      And I have the following incorrectly formatted Certificate of Completion text: "Certificate of Completion sharath chandrareddy nas sucessful completed Macys Introduction to Enactor Certification Test ap 1, 2028 pm Mike Carrell"
      When I enter the provided text into the system
      Then the system should return an error message indicating invalid format

   Scenario: Validate a missing name in the Certificate of Completion
      Given I am a retail system user
      And I have the following Certificate of Completion text: "Certificate of Completion completed Macys Introduction to Enactor Certification Test ap 1, 2028, 217 pm Mike Carrell"
      When I enter the provided text into the system
      Then the system should return an error message indicating missing name

   Scenario: Validate a missing test or training name in the Certificate of Completion
      Given I am a retail system user
      And I have the following Certificate of Completion text: "Certificate of Completion sharath chandrareddy nas sucessful completed ap 1, 2028, 217 pm Mike Carrell"
      When I enter the provided text into the system
      Then the system should return an error message indicating missing test or training name

   Scenario: Validate a missing date in the Certificate of Completion
      Given I am a retail system user
      And I have the following Certificate of Completion text: "Certificate of Completion sharath chandrareddy nas sucessful completed Macys Introduction to Enactor Certification Test pm Mike Carrell"
      When I enter the provided text into the system
      Then the system should return an error message indicating missing date

   Scenario: Validate a missing time in the Certificate of Completion
      Given I am a retail system user
      And I have the following Certificate of Completion text: "Certificate of Completion sharath chandrareddy nas sucessful completed Macys Introduction to Enactor Certification Test ap 2028 Mike Carrell"
      When I enter the provided text into the system
      Then the system should return an error message indicating missing time
 Feature: Verify Certificate of Completion

   Scenario: Verify the presence of Certificate of Completion in a text
       Given I have a text containing a Certificate of Completion
       When I check if the text contains the phrase "Certificate of Completion"
       Then the result should be true

   Scenario: Extract the name from the Certificate of Completion
       Given I have a text containing a Certificate of Completion
       And the name is separated by a space and followed by 'completed'
       When I extract the name from the Certificate of Completion text
       Then the extracted name should be "sharath chandrareddy"

   Scenario: Extract the certificate issuer from the Certificate of Completion
       Given I have a text containing a Certificate of Completion
       And the certificate issuer is separated by a comma and followed by a space
       When I extract the certificate issuer from the Certificate of Completion text
       Then the extracted certificate issuer should be "Mike Carrell"

   Scenario: Verify the date and time of completion in the Certificate of Completion
       Given I have a text containing a Certificate of Completion
       When I extract the date and time of completion from the Certificate of Completion text
       Then the extracted date should be "ap 1, 2028" and the extracted time should be "217 pm"
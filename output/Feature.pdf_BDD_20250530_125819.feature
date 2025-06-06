 Feature: Verifying the Application Updates in the System

   Scenario: Checking for available updates
      Given I am on the application section of the dashboard
      When I check for any available updates
      Then I should see a list of applications with update notifications if available

   Scenario: Updating "vaware Horizon Client"
      Given I have found "vaware Horizon Client - a x VMware Horizon Client" in the list of installed applications with an update notification
      When I initiate the update process for this application
      Then The application should start downloading and installing the latest version
      And After the installation is complete, I should find the updated version number ("vaware Horizon Client - a (new_version) VMware Horizon Client") in the list of installed applications

   Scenario: Launching "vaware Horizon Client" after update
      Given I have found "vaware Horizon Client - a (new_version) VMware Horizon Client" in the list of installed applications
      When I select one instance to launch
      Then The updated VMware Horizon Client application should open with its main interface visible

   Scenario: Checking for new features post update
      Given I have launched the "vaware Horizon Client" after an update
      When I explore the new version of the application
      Then I should find and be able to use the newly added features or improvements

   Feature: Verifying the System Notifications

   Scenario: System sends notifications for important events
      Given I am logged into the system as a user
      When An important event occurs (e.g., account changes, new messages)
      Then I should receive a notification about the event and be able to access it from the notification center

   Scenario: Checking the details of a notification
      Given I have received a notification about an important event
      When I tap on the notification to view its details
      Then I should see the relevant information regarding the event, including date, time, and action required (if any)
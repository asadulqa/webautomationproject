Feature: User Account Registration

  Scenario Outline: Successful account creation
    Given I visit the EverShop homepage
    When I navigate to the signup page
    And And I enter valid registration details "<fullname>", "<password>"
    And I submit the registration form
    Then I should see a welcome message
    Examples:
      | fullname     | password     |
      | Asadul haq   | Password123! |


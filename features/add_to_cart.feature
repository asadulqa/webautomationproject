Feature: Add product to cart

  Scenario: Add a product to the cart successfully
    Given I visit the EverShop
    When I navigate to a product page
    And I add the product to the cart
#    Then I should see the product in the cart

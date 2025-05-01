from behave import *
from page.cart_page import CartPage
from utility.config import EVERSHOP_URL
use_step_matcher("re")


@given("I visit the EverShop")
def step_impl(context):
    context.add_cart_product = CartPage(context.driver)
    context.add_cart_product.visit_url(EVERSHOP_URL)


@when("I navigate to a product page")
def step_impl(context):
    context.add_cart_product.click_on_search_button()


@step("I add the product to the cart")
def step_impl(context):
    context.add_cart_product.add_to_card_product()

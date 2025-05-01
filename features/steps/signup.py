from behave import *
from page.signup_page import SignupPage
import time
from utility.config import EVERSHOP_URL
use_step_matcher("re")


@given("I visit the EverShop homepage")
def step_impl(context):
    context.signup_page = SignupPage(context.driver)
    context.signup_page.visit_url(EVERSHOP_URL)


@when("I navigate to the signup page")
def step_impl(context):
    context.signup_page.click_on_the_man_icon()
    context.signup_page.click_on_create_account()


@step('And I enter valid registration details "(?P<fullname>.+)", "(?P<password>.+)"')
def step_impl(context, fullname, password):
    context.signup_page.enter_credentials_for_create_account(fullname, password)


@step("I submit the registration form")
def step_impl(context):
    context.signup_page.click_on_signup_button()


@then("I should see a welcome message")
def step_impl(context):
    context.signup_page.click_on_the_man_icon()
    context.signup_page.verify_my_account_created_successfully()
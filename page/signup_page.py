from selenium.webdriver.common.by import By
from page.basepage import BasePage
from locators import signup_lc
from time import sleep

class SignupPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def visit_url(self, url):
        self.driver.get(url)

    def click_on_the_man_icon(self):
        man = (By.XPATH,signup_lc.manIconXpath)
        self.wait_for_element(man)
        sleep(2)
        self.click(man)
    def click_on_create_account(self):
        account =(By.XPATH,signup_lc.createAccountXpath)
        self.wait_for_element_clickable(account)
        self.click(account)

    def enter_credentials_for_create_account(self, fullname, password):
        name = (By.XPATH, signup_lc.fullNameXpath)
        passw = (By.XPATH, signup_lc.passwordXpath)
        gmail = (By.XPATH, signup_lc.emailXpath)
        email = self.get_random_email()

        self.wait_for_element(name)
        self.send_keys(name, fullname)

        self.wait_for_element(passw)
        self.send_keys(passw, password)

        self.wait_for_element(gmail)
        self.send_keys(gmail, email)

    def click_on_signup_button(self):
        signup = (By.XPATH,signup_lc.signupButtonXpath)
        self.wait_for_element(signup)
        self.click(signup)

    def verify_my_account_created_successfully(self):
        account =(By.XPATH,signup_lc.myAccountVerifyXpath)
        self.wait_for_element(account)
        my_account = self.get_text(account)
        assert my_account == 'My Account'
        print('My account has created successfully')

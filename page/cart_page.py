from selenium.webdriver.common.by import By
from page.basepage import BasePage
from time import sleep
from selenium.webdriver.common.keys import Keys
from locators import cart_lc

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def visit_url(self, url):
        self.driver.get(url)

    def click_on_search_button(self):
        search = (By.XPATH,cart_lc.searchButtonXpath)
        self.wait_for_element(search)
        self.click(search)
        sleep(2)
        product = (By.XPATH,cart_lc.searchProductXpath)
        self.wait_for_element(product)
        self.send_keys(product, 'Nike react infinity run flyknit')
        sleep(2)
        element = self.driver.find_element(*product)
        element.send_keys(Keys.ENTER)

    def add_to_card_product(self):
        product = (By.XPATH,cart_lc.selectProduct)
        self.wait_for_element(product)
        self.click(product)
        size = (By.XPATH,cart_lc.productSizeXpath)
        color = (By.XPATH,cart_lc.productColorXpath)
        cart = (By.XPATH,cart_lc.addCartButtonXpath)
        self.wait_for_element(size)
        sleep(2)
        self.click(size)
        sleep(2)
        self.wait_for_element(color)
        self.click(color)
        sleep(2)
        self.wait_for_element(cart)
        self.click(cart)

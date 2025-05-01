import string
import os
import random
from enum import Enum
from urllib.parse import unquote
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout


    def find_element(self, locator,timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )


    def find_elements(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )


    def click(self, locator):
        element = self.find_element(locator)
        element.click()


    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def wait_for_element_visible(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )


    def is_element_present(self, locator):
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False


    def hover(self, locator, wait_seconds=2):
        element = self.find_element(locator)
        action_obj = ActionChains(self.driver)
        action_obj.move_to_element(element)
        action_obj.perform()

    def wait_till_element_is_present(self, locator, timeout=10):
        """Wait until the element is present on the page."""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )

    def switch_to_iframe_by_element(self, iframe_element):
        self.driver.switch_to.frame(iframe_element)


    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def find_element_in_iframe(self, locator: By):
        return self.driver.find_element(locator)

    def switch_to_iframe_by_elements(self, locator):
        by, value = locator
        iframe_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        self.driver.switch_to.frame(iframe_element)

    def wait_for_element(self,locator,timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))


    def wait_for_page_loaded(self, timeout=120):
        WebDriverWait(self.driver, timeout).until(PageLoaded())

    def wait_for_element_clickable(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            print(f"Element with locator {locator} was not clickable within {self.timeout} seconds")
            return None


    def double_click(self, locator):
        source = self.find_element(locator)
        action = ActionChains(self.driver)
        action.double_click(source).perform()

    def switch_to_new_window(self, win_handle):
        self.driver.switch_to.window(win_handle)


    def refresh_browser(self):
        self.driver.refresh()


    def get_window_handles(self):
        return self.driver.window_handles



    def get_current_window_handle(self):
        return self.driver.current_window_handle

    def switch_control_to_app(self):
        try:
            self.driver.switch_to.context('NATIVE_APP')
        except Exception as e:
            raise Exception("Unable to switch control to app")


    def get_title(self):
        return self.driver.title

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def back(self):
        self.driver.back()

    def maximize_browser(self):
        self.driver.maximize_window()

    def close_browser(self):
        self.driver.close()

    def generate_random_email(self, prefix="user", domain="example.com"):
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        return f"{prefix}{random_part}@{domain}"


    def scroll_down(self, locator, wait_time=2):
        element = self.find_element(locator)
        try:
            element.send_keys(Keys.PAGE_DOWN)
            element.send_keys(Keys.PAGE_DOWN)
        except Exception as e:
            raise e

    def scroll_up(self, locator, wait_time=2):
        element = self.find_element(locator)
        try:
            element.send_keys(Keys.PAGE_UP)
        except Exception as e:
            raise e

    def click_element(self, locator, method="default"):
        element = self.find_element(locator)

        if method == "default":
            element.click()

        elif method == "javascript":
            self.driver.execute_script("arguments[0].click();", element)

        elif method == "actions":
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()

        elif method == "scroll_and_click":
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()

        elif method == "send_keys":
            element.send_keys(Keys.ENTER)

        else:
            raise ValueError("Unsupported click method specified")



    def is_element_displayed(self, locator):
        element = self.find_element(locator)
        return element.is_displayed()


    def switch_to_frame(self, frame_id):
        self.driver.switch_to_frame(frame_id)


    def __get_by(self, locator_with_strategy):
        """
        Get and return By instance based on the locator strategy
        :param locator_with_strategy: Element locator strategy
        :return: By instance of the element
        """
        if "@@" not in locator_with_strategy:
            locator_with_strategy = Strategy.ID.value + "@@" + locator_with_strategy

        strategy_and_locator = str(locator_with_strategy).split("@@")
        strategy = strategy_and_locator[0]
        locator = strategy_and_locator[1]
        by = None
        if strategy == Strategy.XPATH.value:
            by = (By.XPATH, locator)
        elif strategy == Strategy.ID.value:
            by = (By.ID, locator)
        elif strategy == Strategy.CSS.value:
            by = (By.CSS_SELECTOR, locator)
        elif strategy == Strategy.TAGNAME.value:
            by = (By.TAG_NAME, locator)
        return by


    def get_attribute(self, locator, attribute):
        if isinstance(locator, WebElement):
            return locator.get_attribute(attribute)
        else:
            element = self.find_element(locator)
            return element.get_attribute(attribute)

    def drag_and_drop(self, draggable, droppable):
        try:
            action = ActionChains(self.driver)
            action.drag_and_drop(draggable, droppable).perform()
        except Exception as e:
            raise e

    def select_value_from_dropdown(self, locator, value):
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(value)

    def select_value_from_dropdown_by_index(self, locator, index):
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_index(index)

    def explicit_wait(self, locator):
        element = self.find_element(locator)
        try:
            element = WebDriverWait(
                self.driver, 10).until(
                EC.element_to_be_clickable(element))
        except Exception as e:
            raise e
        return element


    def hit_enter(self, locator, wait_time=2):
        element = self.find_element(locator)
        try:
            element.send_keys(Keys.ENTER)
        except Exception as e:
            raise e

    def check_existence(self, locator):
        try:
            self.driver.find_element(
                *self.__get_by(locator_with_strategy=locator))
            return True
        except Exception as e:
            return False

    def wait_for_element_custom(self, locator):
        count = 0
        flag = False
        while count < 30:
            count = count + 1
            if self.check_existence(locator) is True:
                flag = True
                break
        if not flag:
            print('Element is not loaded: ' + str(locator))
        else:
            print('Element found!')

    def switch_to_main_window(self):
        self.driver.switch_to_default_content()

    def find_child_element(self, element, locator):
        by = self.__get_by(locator_with_strategy=locator)
        return element.find_element(*by)

    def find_child_elements(self, element, locator):
        by = self.__get_by(locator_with_strategy=locator)
        return element.find_elements(*by)

    def get_random_email(self):
        num = random.choice(range(1, 99999999))
        email = "ictusharmathur" + str(num) + "@gmail.com"
        return email


    def scroll_down_index(self, locator, index, wait_time=2):
        """
        Scroll up WebPage
        :param locator: locator
        :param index: number of times down scroll
        :param wait_time: time to wait
        :return:
        """
        element = self.find_element(locator)
        try:
            for i in range(1, index):
                element.send_keys(Keys.DOWN)
        except Exception as e:
            raise e

    def fake_geolocation(self, latitude, longitude):

        try:
            self.driver.execute_cdp_cmd(
                "Browser.grantPermissions",
                {
                    "permissions": ["geolocation"]
                }
            )
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": 100
            }
            self.driver.execute_cdp_cmd(
                "Emulation.setGeolocationOverride", params)
            return self.driver
        except Exception as e:
            raise e

    def press_down_key(self, locator, wait_time=2):

        element = self.find_element(locator)
        try:
            element.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
        except Exception as e:
            raise e

    def press_right_key(self, locator, wait_time=2):

        element = self.find_element(locator)
        try:
            element.send_keys(Keys.ARROW_RIGHT, Keys.RETURN)
        except Exception as e:
            raise e

    def press_left_key(self, locator, wait_time=2):
        element = self.find_element(locator)
        try:
            element.send_keys(Keys.ARROW_LEFT, Keys.RETURN)
        except Exception as e:
            raise e


    def read_browser_console_log(self, log_type='browser'):
        return self.driver.get_log(log_type)


    def accept_alert(self):
        """
        Accepts Java Alert
        :return:
        """
        try:
            self.driver.switch_to_alert().accept()
        except NoAlertPresentException:
            raise NoAlertPresentException

    def dismiss_alert(self):
        """
        Dismiss Java Alert
        :return:
        """
        try:
            self.driver.switch_to_alert().dismiss()
        except NoAlertPresentException:
            raise NoAlertPresentException



    def wait_till_element_is_present_android(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout). \
                until(EC.presence_of_element_located(self.__get_by(locator)))
            return element
        except Exception as e:
            raise e



    def wait_till_element_is_invisible(self, locator, timeout=10):
        web_element = self.find_element(locator)
        try:
            element = WebDriverWait(self.driver, timeout, poll_frequency=2). \
                until(
                EC.invisibility_of_element_located(
                    self.__get_by(locator)))
            return element
        except Exception as e:
            raise e


    def wait_till_url_contains(self, url_substring, timeout=10):
        """
        WebDriver Explicit wait till the current url contains a case-sensitive substring
        :param url_substring: url_substring to be checked
        :param timeout: waiting time
        :return: True when the url matches, TimeoutException otherwise
        """
        try:
            return WebDriverWait(self.driver, timeout). \
                until(EC.url_contains(url_substring))
        except Exception:
            raise TimeoutException(
                f"URL does not contain \"{url_substring}\" substring") from Exception

    def wait_till_method(self, method, timeout=10):
        """
        WebDriver Explicit wait till a custom method is executed.
        Use this method only after you make sure there is no any built-in method in the
        "selenium.webdriver.support.expected_conditions" module for the element you need to wait.
        :param method: method to be checked
        :param timeout: waiting time
        :return: WebElement (can also be True or False) returned by the method
        """
        try:
            return WebDriverWait(self.driver, timeout).until(method)
        except Exception as e:
            raise e

    def teardown_browser(self):
        """
        Close all browser instances
        :return:
        """
        self.driver.quit()


    def disconnect_browser(self):
        """
        Disconnect browser from internet
        :return:
        """
        self.driver.set_network_conditions(
            offline=True,
            latency=1,
            download_throughput=500 * 1024,
            upload_throughput=500 * 1024)

    def connect_browser(self):
        """
        Connect browser with internet
        :return:
        """
        self.driver.set_network_conditions(
            offline=False,
            latency=1,
            download_throughput=500 * 1024,
            upload_throughput=500 * 1024)

    def get_network_conditions(self):
        """
        Gets Chrome network emulation settings
        :return: A dict. For example:
                {'latency': 4, 'download_throughput': 2, 'upload_throughput': 2,
                'offline': False}
        """
        return self.driver.get_network_conditions()

    def print_version(self):
        """
        Prints version
        :return:
        """
        print("print_version = 2.0")


    def get_css_value(self, locator, css_property):
        """"
        This method will get the CSS property of the element
        :return: CSS property Value

        Usage
        get_css_value(locator,"color")
        get_css_value(locator,"font-family")
        get_css_value(locator,"font-size")
        The above code will return value in RGB format such as “rgba(36, 93, 193, 1)”
        """
        element = self.find_element(locator)
        return element.value_of_css_property(css_property)


    def hide_keyboard(self):
        pass

    def switch_control_to_webview(self):
        '''
        Method to switch control to app
        '''
        try:
            webview = self.driver.contexts[1]
            self.driver.switch_to.context(webview)
        except Exception as e:
            raise Exception(
                "Unable to switch control to webview due to " + str(e))

    def handle_pop_up(self, btn_to_click):
        """
        Method to handle (accept/reject) pop ups
        :param btn_to_click: text of the button to be clicked, e.g. "Allow", "Block"
        :return:
        """
        try:
            self.switch_control_to_app()
            self.driver.find_element_by_xpath(
                f".//*[@text='{btn_to_click}']").click()
            self.switch_control_to_webview()
        except Exception as e:
            raise Exception("Unable to handle the pop up due to " + str(e))


    def is_special_char_available(self, url):

        url = unquote(url)
        allowed_ascii = range(128)
        try:
            for literal in url:
                try:
                    if not ord(literal) in allowed_ascii:
                        return True
                except TypeError as e:
                    raise TypeError(str(e), url, literal)
            return False
        except Exception as e:
            raise Exception("Unable to check special character: " + str(e))


    def get_size(self, file):
        """
        Function to check the size of the file
        :return:
        """
        try:
            file_size = os.path.getsize(
                f"C:\\Users\\{os.environ['USERNAME']}\\Downloads\\" + str(file))
            return file_size
        except Exception as e:
            raise Exception("Unable to get file size: " + str(e))

    def remove_file(self, file):
        """
        Function to remove the file from location
        :param file:
        :return:
        """
        if file:
            os.remove(
                f"C:\\Users\\{os.environ['USERNAME']}\\Downloads\\" +
                str(file))

    def get_full_page_screen_shot(self, filename):
        self.driver.save_screenshot(filename)

    def get_page_cookies(self):
        return self.driver.get_cookies()

    def delete_all_cookies(driver):
        driver.delete_all_cookies()


    def get_page_useragent(self):
        return self.driver.execute_script("return navigator.userAgent")

    def get_console_error_logs(self, driver_obj):
        return driver_obj.get_log('browser')

    def switch_to_default(self):
        self.driver.switch_to.default_content()



class PageLoaded:
    def __call__(self, dr):
        ready = dr.execute_script(
            "return document.readyState=='complete';"
        )
        if ready:
            return True
        else:
            return False


class Strategy(Enum):
    """
    Locator Strategy Constants
    """
    XPATH = "xpath"
    ID = "id"
    CSS = "css"
    TAGNAME = "tag name"
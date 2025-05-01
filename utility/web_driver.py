import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

class WebDriverFactory:
    @staticmethod
    def get_driver():
        run_env = os.getenv("RUN_ENV", "local")

        if run_env == "browserstack":
            USERNAME = os.getenv('u')
            ACCESS_KEY = os.getenv("ACCESS_KEY")
            URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

            desired_cap = {
                'os': 'Windows',
                'os_version': '10',
                'browser': 'Chrome',
                'browser_version': 'latest',
                'name': 'Behave Test',
                'build': 'Behave Build',
                'browserstack.local': 'false',
                'browserstack.idleTimeout': 600
            }

            return webdriver.Remote(command_executor=URL, desired_capabilities=desired_cap)

        else:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--start-maximized")

            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)



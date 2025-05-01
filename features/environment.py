from utility.web_driver import WebDriverFactory
import os

def before_scenario(context, scenario):
    context.driver = WebDriverFactory.get_driver()
    if os.getenv("RUN_ENV", "local") != "local":
        context.driver.execute_script(
            f'browserstack_executor: {{ "action": "setSessionName", "arguments": {{"name":"{scenario.name}"}} }}'
        )

def after_scenario(context, scenario):
    if os.getenv("RUN_ENV", "local") != "local":
        if scenario.status == "passed":
            context.driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Scenario passed"}}'
            )
        else:
            context.driver.execute_script(
                f'browserstack_executor: {{ "action": "setSessionStatus", "arguments": {{"status":"failed","reason": "{scenario.exception}"}} }}'
            )

    context.driver.quit()

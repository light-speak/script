from selenium import webdriver
import sys
import argparse

try:
    parser = argparse.ArgumentParser(description='脚本手册')
    parser.add_argument("-S", "--session", help="session", required='true')
    parser.add_argument("-U", "--url", help="ip:port", required='true')
    args = parser.parse_args()
    session = args.session
    url = args.url
except:
    print('error')
    sys.exit()


def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)
    RemoteWebDriver.execute = new_command_execute
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    new_driver = webdriver.Remote(
        command_executor=executor_url, desired_capabilities={}, options=options)
    new_driver.session_id = session_id
    RemoteWebDriver.execute = org_command_execute
    return new_driver


try:
    browser = create_driver_session(session, url)
    browser.quit()

    print('success')
except:
    print('error')

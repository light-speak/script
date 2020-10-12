from selenium import webdriver
import sys
import requests
import argparse
import time

try:
    parser = argparse.ArgumentParser(description='book')
    parser.add_argument("-S", "--session", help="session", required='true')
    parser.add_argument("-U", "--url", help="ip:port", required='true')
    parser.add_argument("-W", "--web", help="address", required='true')

    args = parser.parse_args()
    session = args.session
    url = args.url
    web = args.web
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


run = True
while run == True:
    try:
        browser = create_driver_session(session, url)
        browser.implicitly_wait(5)
    except:
        print('fail: cannot find browser')
        run = False
        sys.exit()
    try:
        browser.switch_to.default_content()
        browser.find_element_by_xpath('//*[@id="composebtn"]')
        userAddr = browser.find_element_by_xpath('//*[@id="useraddr"]').text
        print(userAddr)
        requests.get(web, params={'status': 'enable','mail':userAddr})
    except:
        print('fail: cannot find element')
        requests.get(web, params={'status': 'disable'})
    time.sleep(10)

# http://127.0.0.1:55964
# f15e94766c8155e15c6cc7e691b40bc7

from selenium import webdriver
import sys
from browsermobproxy import Server
import time


server = Server(
    "/Users/linty/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()
proxy.new_har("test", options={'captureHeaders': True, 'captureContent': True})

print(proxy.proxy)


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
    options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    options.add_argument("--no-sandbox")
    new_driver = webdriver.Remote(
        command_executor=executor_url, desired_capabilities={}, options=options)
    new_driver.session_id = session_id
    RemoteWebDriver.execute = org_command_execute
    return new_driver


browser = create_driver_session(
    'f15e94766c8155e15c6cc7e691b40bc7', 'http://127.0.0.1:55964')
browser.implicitly_wait(5)
browser.refresh()
time.sleep(10)
browser.execute_script(
    'window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)

result = proxy.har  # 返回值
for entry in result['log']['entries']:  # 循环获取需要的内容
    _url = entry['request']['url']
    print(_url)
# browser.quit()

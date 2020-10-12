
from selenium import webdriver
import sys
import signal
from browsermobproxy import Server
import time


def handler(signal_num, frame):
    print(u"\n退出程序")
    sys.exit(signal_num)


server = Server(
    "/Users/linty/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()
proxy.new_har("test", options={'captureHeaders': True, 'captureContent': True})


signal.signal(signal.SIGINT, handler)


option = webdriver.ChromeOptions()
option.add_argument("--no-sandbox")
option.add_argument('--proxy-server={0}'.format(proxy.proxy))

# option.add_argument('window-size=1920x1080')
# option.add_argument('--disable-gpu')
# option.add_argument('--headless')


browser = webdriver.Chrome(executable_path=sys.path[0] + "/chromedriver",
                           options=option)


url = ("http://hg7.live/")


browser.implicitly_wait(5)

browser.get(url)
time.sleep(30)
browser.get('http://hg7.live/#/pages/Home/ClassListPage/index?navId=879&type=2&moduleId=25')

result = proxy.har
for entry in result['log']['entries']:
    _url = entry['request']['url']
    print(_url)
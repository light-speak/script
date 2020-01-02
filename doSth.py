
import requests
import signal
import argparse
import random
import time
import sys
import logging
import datetime

from selenium import webdriver

from pyvirtualdisplay import Display

from url_list import urlList,sourceUrlList
from user_agent import userAgent

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("%s.txt" % datetime.date.today() )
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 传入参数
parser = argparse.ArgumentParser(description='脚本手册')
parser.add_argument("--times", type=int, default="1")
parser.add_argument("--wait",type=int, default="10")
parser.add_argument("--useProxy", type=int, default="true")
args = parser.parse_args()
times = args.times
wait = args.wait
useProxy = args.useProxy

successTime = 0

useList = []
agentSize = len(userAgent)
sourceUrlSize = len(sourceUrlList)

display = Display(visible=0, size=(1920, 1080))
display.start()

browserList = []

def start():
    global display
    global successTime
    print(
        "╔════════════════════════════ 程序开始运行 ════════════════════════════╗")
    time.sleep(0.3)
    browser: webdriver
    print("╠                                                                      ╣")
    time.sleep(0.3)
    print("╠════════════════════════════ 网址加载成功 ════════════════════════════╣")
    if useProxy == 1:
        print_one_by_one(
            "╠════════════════════════════ 代理加载成功 ════════════════════════════╣")
        print("╠                                                                      ╣")
    while True:
        if successTime >= times:
            break
        if useProxy == 1:
            browser = initClient(True)
        else:
            browser = initClient(False)
        url = getUrl()
        browserList.append(browser)
        print("                                                                                                                                                             ",end="\r")
        sourceUrl = sourceUrlList[random.randint(0, sourceUrlSize - 1)]
        print_one_by_one("╠═ 已成功次数: %s 来源网址: %s" % (successTime,sourceUrl),False)
        browser.get(sourceUrl)
        time.sleep(5)
        print_one_by_one("╠═ 已成功次数: %s 来源网址: %s 网址标题: %s" % (successTime,sourceUrl,browser.title),False)
        browser.execute_script("window.location.href='%s';" % (url))
        print_one_by_one("╠═ 跳转网址中...............",False)
        print_one_by_one("╠═ 已成功次数: %s 来源网址: %s 当前网址: %s" % (successTime,sourceUrl,url),False)
        for i in range(1, random.randint(0,5)):
            browser.execute_script("window.location.href='%s';" % (url))
            for i in range(1, wait):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)
        successTime += 1
        print_one_by_one("╠═ 已成功次数: %s 来源网址: %s 当前网址: %s 网址标题: %s" % (successTime, sourceUrl, url, browser.title),False )
        browserList.remove(browser)
        browser.quit()
        logger.info("成功数量 %s" % successTime)
    for browser in browserList:
        browser.quit()
    display.stop()
    sys.exit(signal_num)
def getUrl():
    global useList
    if len(urlList) == 0:
        print("╠                                                                      ╣")
        print(
            "╠════════════════════════!! 网站列表不得为空 !!════════════════════════╣")
        sys.exit()
    if len(useList) == 0:
        useList = urlList.copy()
    url = useList.pop()
    return url


def initClient(useProxy):
    global agentSize
    option = webdriver.ChromeOptions()
    option.add_argument("--no-sandbox")
    # 伪装浏览器
    option.add_argument(
        "user-agent=%s" % userAgent[random.randint(0, agentSize - 1)])
    option.add_argument(
        "x-forwarded-for=%s" % "123,123,123,123"
    )
    if useProxy:
        option.add_argument("-proxy-server=")
    browser = webdriver.Chrome(
        executable_path= sys.path[0] + "/chromedriver", options=option)
    return browser

def print_one_by_one(line, newLine=True):
    for i in range(len(line)):
        if newLine and i == len(line) - 1:
            print("\r"+line[0:i+1])
        else:
            print("\r"+line[0:i+1], end="")
        time.sleep(0.01)


def handler(signal_num,frame):
    print("\n退出程序")
    for browser in browserList:
        browser.quit()
    display.stop()
    sys.exit(signal_num)
signal.signal(signal.SIGINT, handler)

start()

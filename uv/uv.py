#! /usr/bin/env python3
import requests
import signal
import argparse
import random
import time
import sys
import logging
import datetime

from progressbar import *

from selenium import webdriver

from pyvirtualdisplay import Display

from url_list import urlList, sourceUrlList
from user_agent import userAgent

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("%s.txt" % datetime.date.today())
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 传入参数
# parser = argparse.ArgumentParser(description='脚本手册')
# parser.add_argument("--maxtimes", type=int, default="10")
# parser.add_argument("--mintimes", type=int, default="1")
# parser.add_argument("--max", type=int, default="100")
# parser.add_argument("--min", type=int, default="10")
# parser.add_argument("--useProxy", type=int, default="0")
# args = parser.parse_args()

# 最大次数
maxtimes = 5
# 最小次数
mintimes = 1
# 是否使用代理(暂时无用)
useProxy = 0
# 最大停留时间
Max = 10
# 最小停留时间
Min = 5

# 每轮完成后,最大等待时间
MaxWait = 300
# 每轮完成后,最小等待时间
MinWait = 100



times = random.randint(mintimes, maxtimes)
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

    useNewBrowser = False
    back = False

    print(
        "╔════════════════════════════ 程序开始运行 ════════════════════════════╗")
    time.sleep(0.3)
    browser: webdriver
    # print("╠                                                                      ╣")
    time.sleep(0.3)
    print("╠════════════════════════════ 网址加载成功 ════════════════════════════╣")
    if useProxy == 1:
        print_one_by_one(
            "╠════════════════════════════ 代理加载成功 ════════════════════════════╣")
        print("╠                                                                      ╣")
    guess = (5 * ((Min + Max) // 2) + 10 + ((MaxWait + MinWait) / 2)) * times
    print("╠ 程序运行次数: %s, 程序预计运行时间: %s 分钟" % (times, guess // 60 ))
    while True:
        if successTime >= times:
            break
        if useProxy == 1 and useNewBrowser:
            browser = initClient(True)
        else:
            browser = initClient(False)
        url = getUrl()
        browserList.append(browser)
        print("                                                                                                                                                             ", end="\r")
        sourceUrl = sourceUrlList[random.randint(0, sourceUrlSize - 1)]
        print_one_by_one("╠═ 已成功次数: %s 来源网址: %s" %
                         (successTime, sourceUrl), False)
        browser.get(sourceUrl)
        time.sleep(10)
        print_one_by_one("╠═ 已成功次数: %s 来源网址: %s 网址标题: %s" %
                         (successTime, sourceUrl, browser.title), False)
        browser.execute_script("window.location.href='%s';" % (url))
        print_one_by_one("╠═ 跳转网址中...............", False)
        print_one_by_one("╠═ 已成功次数: %s 来源网址: %s 当前网址: %s" %
                         (successTime, sourceUrl, url), False)
        randomRound = random.randint(3, 7)
        randomWait = random.randint(Min, Max)
        print("\n╠═ 循环次数: %s 等待时间 %s 秒" % (randomRound, randomWait))
        total = randomRound * randomWait - 1
        widgets = ['╠═ ', Percentage(), ' ', Bar('#'), ' ', Timer()]
        pbar = ProgressBar(widgets=widgets, maxval=10*total).start()

        for i in range(0, randomRound):
            if back:
                browser.back()
            if i != 0:
                list_a = browser.find_elements_by_tag_name("a")
                if len(list_a) != 0:
                    a = list_a[random.randint(0, len(list_a)-1)]
                    newUrl = a.get_attribute("href")
                    if newUrl is not None and "javascript" not in newUrl:
                        if random.randint(0, 10) > 8:
                            browser.get(newUrl)
                            back = True
                    else:
                        if random.randint(0, 10) > 8:
                            browser.refresh()
            for j in range(0, randomWait):
                browser.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)
                pbar.update(10 * (i * randomWait + j))
        successTime += 1
        pbar.finish()
        browserList.remove(browser)

        if random.randint(0, 10) > 2:
            browser.quit()
            useNewBrowser = True
        else:
            useNewBrowser = False
        logger.info("成功数量 %s" % successTime)

        widgets = ['╠═ ', Percentage(), ' ', Bar('#'), ' ', Timer()]
        randomOverWait = random.randint(MinWait,MaxWait)
        pbar = ProgressBar(widgets=widgets, maxval=10*randomOverWait).start()
        print(
            "╠════════════════════════════ 程序等待%s秒 ════════════════════════════╣" % (randomOverWait))
        for i in range(0,randomOverWait):
            time.sleep(1)
            pbar.update(10 * i)
        pbar.finish()
    for browser in browserList:
        browser.quit()
    display.stop()
    print("╠════════════════════════!! 程序已经成功退出 !!════════════════════════╣")

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
    if useProxy:
        option.add_argument("-proxy-server=")
    browser = webdriver.Chrome(
        executable_path=sys.path[0] + "/chromedriver", options=option)
    return browser


def print_one_by_one(line, newLine=True):
    for i in range(len(line)):
        if newLine and i == len(line) - 1:
            print("\r"+line[0:i+1])
        else:
            print("\r"+line[0:i+1], end="")
        time.sleep(0.01)


def handler(signal_num, frame):
    print("\n退出程序")
    for browser in browserList:
        browser.quit()
    display.stop()
    sys.exit(signal_num)


signal.signal(signal.SIGINT, handler)

start()

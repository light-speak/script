import random
import time
import sys
import signal


from selenium import webdriver
from msg import msgs

import argparse

parser = argparse.ArgumentParser(description='脚本手册')
parser.add_argument("-T", "--times", help="每次消息发送次数", default="3")
parser.add_argument("-P", "--proxyfile", help="代理文件", required="true")
args = parser.parse_args()
times = int(args.times)
proxyfile = args.proxyfile

browserList = []


def send_message():
    iframe = browser.find_element_by_name("chat")
    browser.switch_to.frame(iframe)
    # 消息框
    input_content = browser.find_element_by_id('_MEIQIA_INPUT')
    # 提交按钮
    button = browser.find_element_by_class_name('grIjqJ')
    # button = browser.find_element_by_class_name('jNTBPW')

    for i in range(0, int(times)):
        # 选择随机的消息
        msg = random.choice(msgs)
        input_content.send_keys(msg)
        button.click()
        time.sleep(3)


file = open(proxyfile, 'r')
proxyList = file.readlines()

count = 1
for proxy in proxyList:
    if count > times:
        print('执行完成')
        break
    count += 1
    try:
        option = webdriver.ChromeOptions()
        option.add_argument("-proxy-server=%s" % (proxy))
        option.add_argument("--no-sandbox")
        option.add_argument('--disable-gpu')
        # option.add_argument('--headless')

        browser = webdriver.Chrome(executable_path=sys.path[0] + "/chromedriver",
                                   options=option)
        browserList.append(browser)
        browser.set_page_load_timeout(30)

        browser.get(url='https://mmm7219.com/')

        time.sleep(2)
        browser.execute_script("window.location.href='%s';" % (
            'https://temp-chat.mstatik.com/widget/standalone.html?eid=205373'))
        browser.implicitly_wait(5)
        send_message()
        print('成功')
    except Exception as e:
        print(e)
        for b in browserList:
            b.quit()
        print('失败')
        continue


def handler(signal_num, frame):
    print("\n退出程序")
    for browser in browserList:
        browser.quit()
    sys.exit(signal_num)


signal.signal(signal.SIGINT, handler)

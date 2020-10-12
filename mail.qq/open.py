from selenium import webdriver
import sys
import signal
import time
import os
import requests
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image, ImageEnhance
import uuid
import argparse

parser = argparse.ArgumentParser(description='脚本手册')
parser.add_argument("-Q", "--qq", help="发送邮件的QQ号", required='true')
parser.add_argument("-P", "--pas", help="发送邮件的密码", required='true')
args = parser.parse_args()
qq = args.qq
pas = args.pas


def handler(signal_num, frame):
    print(u"\n退出程序")
    sys.exit(signal_num)


signal.signal(signal.SIGINT, handler)


def get_ewm(img_adds):
    if os.path.isfile(img_adds):
        img = Image.open(img_adds)
    else:
        rq_img = requests.get(img_adds).content
        img = Image.open(BytesIO(rq_img))

    txt_list = pyzbar.decode(img)
    res = ''
    for txt in txt_list:
        barcodeData = txt.data.decode()
        res += barcodeData
    return res


option = webdriver.ChromeOptions()
option.add_argument("--no-sandbox")
option.add_argument('window-size=1920x1080')
# option.add_argument('--disable-gpu')
# option.add_argument('--headless')

browser = webdriver.Chrome(executable_path=sys.path[0] + "/chromedriver",
                           options=option)


url = ("https://mail.qq.com/")
browser.get(url)

browser.implicitly_wait(5)
# time.sleep(3)

browser.switch_to.frame("login_frame")  # 理论上这条不会错
usePass = True
content = 'nothing'

try:
    name = (qq)
    key = (pas)
    # 定位至账号密码登录
    browser.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
    # 账号，密码输入
    browser.find_element_by_xpath('//*[@id="u"]').send_keys(name)
    browser.find_element_by_xpath('//*[@id="p"]').send_keys(key)
    # 点击登录
    browser.find_element_by_xpath('//*[@id="login_button"]').click()
    # 寻找写信
    browser.find_element_by_xpath('//*[@id="composebtn"]')
    # 如果上面出错了, 就扫码登录吧
except:
    usePass = False

if usePass == False:
    browser.find_element_by_xpath(
        '//*[@id="switcher_qlogin"]').click()
    qrImage = browser.find_element_by_xpath(
        '//*[@id="qrlogin_img"]')
    path = str(uuid.uuid1()) + '.png'

    qrImage.screenshot(path)
    content = get_ewm(path)
    os.remove(path)

service = browser.command_executor._url
session = browser.session_id
print('%s|%s|%s' % (content, service, session))

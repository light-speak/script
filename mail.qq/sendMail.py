# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import argparse

# jhkmcebolhzwbcgb
parser = argparse.ArgumentParser(description='脚本手册')
parser.add_argument("-Q", "--qq", help="发送邮件的QQ号", required='true')
parser.add_argument("-P", "--pas", help="发送邮件的密码", required='true')
parser.add_argument("-T", "--target", help="目标邮箱", required='true')
parser.add_argument("--title", help="邮件主题", required='true')

parser.add_argument("-C", "--content",  help="发送内容", required='true')
# SL 来源语言 TL 目标语言  S 目标文件
args = parser.parse_args()

qq = args.qq
pas = args.pas
target = args.target
content = args.content
title = args.title

try:
    option = webdriver.ChromeOptions()
    option.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path=sys.path[0] + "/chromedriver", options=option)

    url = ("https://mail.qq.com/")
    name = (qq)
    key = (pas)
    out_name = (target)
    #
    # 打开浏览器
    driver.get(url)
    driver.implicitly_wait(10)

    # 最大化窗口
    # driver.maximize_window()

    # 切换iframe
    driver.switch_to.frame("login_frame")

    # 定位至账号密码登录
    driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()

    # 账号，密码输入
    driver.find_element_by_xpath('//*[@id="u"]').send_keys(name)
    driver.find_element_by_xpath('//*[@id="p"]').send_keys(key)

    # 点击登录
    driver.find_element_by_xpath('//*[@id="login_button"]').click()

    time.sleep(2)
    # 点击头像登录
    # driver.find_element_by_xpath('//*[@id="img_out_874335483"]').click()

    # 点击写信
    driver.find_element_by_xpath('//*[@id="composebtn"]').click()
    time.sleep(1)

    # 切换iframe至写信
    driver.switch_to.frame("mainFrame")
    # driver.switch_to.frame(driver.find_element_by_id('mainFrame'))
    time.sleep(1)

    # 添加收件人
    driver.find_element_by_xpath(
        '//*[@id="toAreaCtrl"]/div[2]/input').send_keys(out_name)

    # 添加主题
    driver.find_element_by_xpath('//*[@id="subject"]').send_keys(title)

    # 退出当前编辑Iframe
    driver.switch_to.default_content()

    # 切换Iframe至编辑正文
    driver.switch_to.frame("mainFrame")
    # Body_frame=driver.find_element_by_xpath('//iframe[@scrolling="auto"]')
    Body_frame = driver.find_element_by_class_name("qmEditorIfrmEditArea")
    driver.switch_to.frame(Body_frame)

    # 添加正文
    driver.find_element_by_xpath('/html/body').send_keys(content)
    time.sleep(1)

    # 退回大Frame再点击发送
    driver.switch_to.parent_frame()
    driver.find_element_by_xpath('//*[@id="toolbar"]/div/a[1]').click()
    time.sleep(1)
    driver.quit()
    print("发送完成")
    sys.exit()
except:
    driver.quit()
    print("发送失败")
    sys.exit()

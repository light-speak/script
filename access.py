

import requests
import threading
import time
import random
from selenium import webdriver

# 是否点击链接跳转
DUMP = 1
# 超时时间
WAIT_TIME = 8
# 线程数量
THREAD_NUM = 1
# 链接列表
urlList = [
    "http://zz.zfzy06.com/"
]
# 芝麻代理隧道  返回格式为JSON
proxyApi = "http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&pack=62869&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
# 浏览器特征列表
user_agent = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11'
]
# 来源
referer = "http://www.gov.cn/"

useList = []
agentSize = len(user_agent)
count = 0
proxyList = []


def job():
    global proxyList
    global count
    global useList
    global urlList
    global proxyApi
    global agentSize
    global WAIT_TIME
    global user_agent
    global DUMP
    global referer

    success = 0
    while True:
        if len(proxyList) == 0:
            res = requests.get(proxyApi).json()
            if res['code'] != 0:
                print("get proxy field")
                time.sleep(3)
            else:
                # print(res)
                proxyList = res['data']
        else:
            if len(useList) == 0:
                useList = urlList.copy()
            url = useList.pop()

            proxy = proxyList.pop()
            ip = proxy['ip']
            port = proxy['port']

            opt = webdriver.ChromeOptions()
            opt.add_argument("-proxy-server=http://%s:%s" % (ip, port))
            agent = user_agent[random.randint(0, agentSize-1)]
            # print(agent)
            opt.add_argument("user-agent=%s" % (agent))

            browser = webdriver.Chrome(
                executable_path="/data/script/chromedriver", options=opt)
            browser.get(referer)
            time.sleep(1)
            browser.execute_script("window.location.href='%s';" % (url))
            for i in range(1, WAIT_TIME):
                browser.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight)')
                nowUrl = browser.current_url
                print("===========已成功数量 %s =========== 当前访问的网址是 %s" %
                      (count, url), end="\r")
                # print(nowUrl)
                if nowUrl.find(url, 0, len(nowUrl)) == -1:
                    success = 1
                    break
                time.sleep(1)
                if i == WAIT_TIME:
                    print("%s跳转超时" % (url))
                    browser.quit()
            if success == 1:
                time.sleep(random.randint(0, 120))
                if DUMP == 1:
                    time.sleep(1)
                    url = browser.find_element_by_tag_name(
                        "a").get_attribute("href")
                    print(url)
                    browser.get(url)
                    for i in range(1, 3):
                        browser.execute_script(
                            'window.scrollTo(0, document.body.scrollHeight)')
                        time.sleep(1)
                count += 1
                browser.quit()


for i in range(0, THREAD_NUM):
    t = threading.Thread(target=job)
    t.start()

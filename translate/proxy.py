# @Time:        2020/1/4
# @File :       快代理.py
# @Software:    PyCharm
# 课题：         爬取快代理（爬取ip代理，构建ip代理池）
# Method:       requests
# tools：        1.parsel
#                2.xpath


import requests
import parsel
import time

def check_ip(proxies_list):
    """检查代理IP的方法"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    can_use = []
    for proxy in proxies_list:
        try:
            # url:路由地址,headers:请求头,proxies:代理,
            response_2 = requests.get(url='https://www.baidu.com', headers=headers, proxies=proxy, timeout=0.1)
            if response_2.status_code == 200:
                can_use.append(proxy)
        except Exception as e:
            print(e)
    return can_use


# 爬虫思路(爬虫是模拟浏览器进行请求然后进行数据保存)
# 1·确定爬取的url路径，网站的headers参数
def send_request(page):
    print("+++++++正在抓取第{}页数据++++++++++++++".format(page))
    base_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    # 2·发送请求 --request 模拟浏览器发送请求，获取响应数据
    response = requests.get(base_url, headers=headers)
    data = response.text
    time.sleep(1)
    return data
    # print(data)


def parse_data(data):
    # 3·解析数据 --parsel模块 转化为selector对象，selector具有xpath语法,能够对数据进行处理
    # 3.1转换为python的数据类型
    html_data = parsel.Selector(data)
    # 3.2解析数据
    parse_list = html_data.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
    # print(parse_list)
    return parse_list

if __name__ == '__main__':
    proxies_list = []
    # proxies_spider()

    for page in range(1,5):
        data = send_request(page)
        parse_list = parse_data(data)

        # 二次提取
        for tr in parse_list:
            proxies_dict = {}
            http_type = tr.xpath('./td[4]/text()').extract_first()
            ip_num = tr.xpath('./td[1]/text()').extract_first()
            port_num = tr.xpath('./td[2]/text()').extract_first()
            # print(http_type,ip_num,port_num)

            # 构建代理ip的字典
            proxies_dict[http_type] = ip_num + ":" + port_num
            # print(proxies_dict)
            proxies_list.append(proxies_dict)

    print('获取到的代理ip的数量为：', len(proxies_list), '个')
    can_use = check_ip(proxies_list)
    print('能用的代理ip的数量为：', len(can_use), '个')

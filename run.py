# -*- coding: utf-8 -*-
#__author__="ZJL"


from common.redis_manager import RedisManager
from common.request_manager import RequestManager
from common.request_common import asyncRetry
from common.url_manager import UrlManager
from common.ip_db_manager import Ip_DBSave
from bs4 import BeautifulSoup as bs
import asyncio
import time
import random
import requests

# 公用头信息
headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }

# 存IP
rdb = RedisManager(db="4")

# 这个没有用摆设
rm = UrlManager()

# 重试机制
@asyncRetry(4, rm.add_error_url)
async def getPage(url):
    # asyncio.Semaphore(),限制同时运行协程数量
    sem = asyncio.Semaphore(5)
    with (await sem):
        async with RequestManager().session as session:
            async with session.get(url, headers=headers, timeout=360) as resp:
                # 暂停一会儿，太不暗落落容易被封
                time.sleep(random.random()*5)
                # 断言，判断网站状态
                assert resp.status == 200
                # 判断不同url做不同的处理
                if "xicidaili" in url:
                    body = await resp.text()
                    xici_grabPage(url,body)
                elif "kuaidaili" in url:
                    body = await resp.text()
                    kuaidaili_grabPage(url,body)
                elif "nianshao" in url:
                    body = await resp.text()
                    nianshao_grabPage(url,body)
                elif "66ip" in url:
                    body = await resp.text()
                    ip66_grabPage(url,body)
                elif "httpsdaili" in url:
                    body = await resp.text()
                    httpsdaili_grabPage(url,body)
                elif "swei360" in url:
                    body = await resp.text()
                    swei360_grabPage(url,body)
                elif "kxdaili" in url:
                    body = await resp.text()
                    kxdaili_grabPage(url,body)
                else:
                    return await resp.text()
                # 关闭请求
                session.close()

# 各个网站的不同解析函数
def xici_grabPage(url,body):
    try:
        soup = bs(body, "lxml")
        trs = soup.find(id="ip_list").find_all("tr")
        for index, tr in enumerate(trs):
            if index > 0:
                for index, td in enumerate(tr.find_all("td")):
                    if index == 1:
                        ip = td.text
                    elif index == 2:
                        port = td.text
                checkout_ip(ip + ":" + port,url)
    except Exception as e:
        return e, "xici_grabPage"

def kuaidaili_grabPage(url,body):
    try:
        soup = bs(body, "lxml")
        trs = soup.find(id="list").find_all("tr")
        for index, tr in enumerate(trs):
            if index > 0:
                for index, td in enumerate(tr.find_all("td")):
                    if index == 0:
                        ip = td.text
                    elif index == 1:
                        port = td.text
                print(ip + ":" + port)
                checkout_ip(ip + ":" + port,url)
    except Exception as e:
        return e, "kuaidaili_grabPage"

def nianshao_grabPage(url,body):
    try:
        soup = bs(body, "lxml")
        trs = soup.find(class_="table").find_all("tr")
        for index, tr in enumerate(trs):
            if index > 0:
                for index, td in enumerate(tr.find_all("td")):
                    if index == 0:
                        ip = td.text
                    elif index == 1:
                        port = td.text
                print(ip + ":" + port)
                checkout_ip(ip + ":" + port,url)
    except Exception as e:
        return e, "nianshao_grabPage"

def ip66_grabPage(url,body):
    try:
        soup = bs(body, "lxml")
        trs = soup.find("table", width='100%').find_all("tr")
        for index, tr in enumerate(trs):
            if index > 0:
                for index, td in enumerate(tr.find_all("td")):
                    if index == 0:
                        ip = td.text
                    elif index == 1:
                        port = td.text
                print(ip + ":" + port)
                checkout_ip(ip + ":" + port,url)
    except Exception as e:
        return e, "ip66_grabPage"

def httpsdaili_grabPage(url,body):
    try:
        soup = bs(body, "lxml")
        trs = soup.find("table", class_="table table-bordered table-striped").find_all("tr")
        for index, tr in enumerate(trs):
            if index > 0:
                for index, td in enumerate(tr.find_all("td")):
                    if index == 0:
                        ip = td.text
                    elif index == 1:
                        port = td.text
                print(ip + ":" + port)
                checkout_ip(ip + ":" + port,url)
    except Exception as e:
        return e, "httpsdaili_grabPage"

def swei360_grabPage(url,body):
    try:
        soup = bs(body, "lxml")
        trs = soup.find("div", id="list").find_all("tr")
        for index, tr in enumerate(trs):
            if index > 0:
                for index, td in enumerate(tr.find_all("td")):
                    if index == 0:
                        ip = td.text
                    elif index == 1:
                        port = td.text
                print(ip + ":" + port)
                checkout_ip(ip + ":" + port,url)
    except Exception as e:
        return e, "swei360_grabPage"

def kxdaili_grabPage(url,body):
    try:
        soup = bs(body, "lxml")
        trs = soup.find("table", class_="ui table segment").find_all("tr")
        for index, tr in enumerate(trs):
            if index > 0:
                for index, td in enumerate(tr.find_all("td")):
                    if index == 0:
                        ip = td.text
                    elif index == 1:
                        port = td.text
                print(ip + ":" + port)
                checkout_ip(ip + ":" + port,url)
    except Exception as e:
        return e, "kxdaili_grabPage"

# IP有效性检查，去访问百度
def  checkout_ip(ip_port,xurl=""):
    s = requests.session()
    try:
        proxies={
            "http":"http://"+ip_port,
        }
        url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=python&rsv_pq=b3fb9f5200036a4f&rsv_t=04cdhQxxUlftjer%2FovL4Xb6B2ySx%2F%2BMhjXIPfJV24Ezf7GRFVpuhiYmxzmw&rqlang=cn&rsv_enter=1&rsv_sug3=7&rsv_sug1=1&rsv_sug7=100&rsv_sug2=0&inputT=2391&rsv_sug4=3002&rsv_sug=2"
        # url = "http://www.ip181.com/"
        r = s.get(url, headers=headers, proxies=proxies,timeout=360)
        time.sleep(random.random() * 2)
        assert r.status_code == 200
    except Exception as e:
        return e,"checkout_ip"
    else:
        print(xurl+" "+ip_port+" OK")
        ip_time = time.time()
        db_name = "proxyIP"
        Ip_DBSave(rdb, db_name, ip_port, ip_time)
    finally:
        s.close()

def main():
    # 总页数
    page_num = 5
    # 起始页面
    page_url_base = [
        'http://www.xicidaili.com/nn/',
        'http://www.kuaidaili.com/free/inha/',
        'http://www.nianshao.me/?page=',
        'http://www.66ip.cn/',
        # 'http://www.goubanjia.com/free/anoy/%E9%AB%98%E5%8C%BF/',
        'http://www.httpsdaili.com/?page=',
        'http://www.swei360.com/free/?stype=1&page=',
        'http://www.kxdaili.com/dailiip/1/'
    ]

    # 所有URL的列表
    page_urls = []
    for url in page_url_base:
        if "66ip" in url or "kxdaili" in url :
            for num in range(1, page_num + 1):
                new_url = url + str(num) +".html"
                page_urls.append(new_url)
        elif "goubanjia" in url :
            for num in range(1, page_num + 1):
                new_url = url + "index" + str(num) + ".shtml"
                page_urls.append(new_url)
        else:
            for num in range(1,page_num+1):
                new_url = url + str(num)
                page_urls.append(new_url)
    # asyncio.get_event_loop()，创建事件循环
    loop = asyncio.get_event_loop()
    # 协程任务
    tasks = [getPage(host) for host in page_urls]
    # 在事件循环中执行协程程序
    loop.run_until_complete(asyncio.gather(*tasks))
    # 关闭
    loop.close()


if __name__ == '__main__':
    # start = time.time()
    while True:
        main()
        time.sleep(6000*2)
    # print("Elapsed Time: %s" % (time.time() - start))


'''
http://www.xicidaili.com/nn/4
http://www.kuaidaili.com/free/inha/8/
http://www.data5u.com/
http://www.66ip.cn/3.html
http://www.nianshao.me/?page=2
http://www.goubanjia.com/free/anoy/%E9%AB%98%E5%8C%BF/index2.shtml
http://www.httpsdaili.com/?page=3
http://www.swei360.com/free/?stype=1&page=2
'''


# t = time.time()
# print(t)
# db_name = "proxyIP"
#
# rd = RedisManager(db="1")
#
# rd.setKeyValue(db_name,"111","222a")
# rd.setKeyValue(db_name,"112","222b")
# rd.setKeyValue(db_name,"122","222c")
# rd.setKeyValue(db_name,"322","222d")
#
# a = rd.getKeyAllAttribute(db_name)
# lena = len(a)
# print("len",lena)
# print(random.randint(0,lena-1))
# a.sort( reverse=True)
# print(a)
# print(a[-1])
# # print(rd.delAttribute(db_name,a[-1]))
# print(rd.getKeyAllAttribute(db_name))
# print(rd.getKeyValue(db_name,a[random.randint(0,lena-1)]))
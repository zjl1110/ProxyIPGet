# -*- coding: utf-8 -*-
#__author__="ZJL"

from common.ip_db_manager import Ip_DBGetAll
from common.redis_manager import RedisManager
import requests
import time
import random

headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

# 不停校验库内IP是否有效
def checkout_IP():
    rdb = RedisManager(db="4")
    db_name = "proxyIP"
    ip_list = Ip_DBGetAll(rdb,db_name)
    for ip,ip_time in ip_list.items():
        web_checkout_ip(rdb, db_name, ip, ip_time)

# 去百度校验IP是否有效
def  web_checkout_ip(rm, db_name, ip_port, ip_time):
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
        print(r.status_code)
        print("DEL",rm.delAttribute(db_name,ip_time))
        return e,"checkout_ip"
    else:
        print(r.status_code)
    finally:
        s.close()

def main():
    checkout_IP()

if __name__ == '__main__':
    while True:
        main()

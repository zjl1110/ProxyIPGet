# -*- coding: utf-8 -*-
#__author__="ZJL"


import requests

headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }

s = requests.session()
proxies={
    "http":"http://119.5.1.5:808",
    "https":"https://119.5.1.5:808"
}
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}
r = s.get('http://1212.ip138.com/ic.asp',headers=headers,proxies=proxies)
print(r.status_code)
print(r.text)

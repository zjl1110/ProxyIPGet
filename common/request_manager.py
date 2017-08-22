# -*- coding: utf-8 -*-
#__author__="ZJL"

import aiohttp


# 请求管理器
class RequestManager(object):
    def __init__(self):
        self.session = aiohttp.ClientSession()

    def get(self, url, *, allow_redirects=True, **kwargs):
        return self.session.get(url, allow_redirects=True, **kwargs)

    def post(self, url, *, data=None, **kwargs):
        return self.session.post(url, data=None, **kwargs)
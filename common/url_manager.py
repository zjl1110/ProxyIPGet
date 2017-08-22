# -*- coding: utf-8 -*-
#__author__="ZJL"

from common.redis_manager import RedisManager as rm


# Url管理器

class UrlManager(object):
    # new_urls是待爬URL队列名，old_urls是已爬URL队列名，error_urls是失败URL队列名
    def __init__(self, new_urls="new_urls", old_urls="old_urls", error_urls="error_urls", **key):
        # redis队列
        self.rm = rm()
        # 待爬url
        self.new_urls = new_urls
        # 已爬url
        self.old_urls = old_urls
        # 失败url
        self.error_urls = error_urls

        # 向管理器中添加一个新的url

    def add_new_url(self, url):
        if url is None:
            return
            # 如果不在待爬中也不再已爬中就添加新url
        if not self.rm.isExist(self.new_urls, url) and not self.rm.isExist(self.old_urls, url):
            self.rm.setSets(self.new_urls, url)

            # 向管理器中添加一个失败的url

    def add_error_url(self, url):
        if url is None:
            return
        self.rm.setSets(self.error_urls, url)

        # 向管理器中添加新的更多的url

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

            # 判断管理器是否有新的待爬取的url

    def has_new_url(self):
        return self.rm.setsLen(self.new_urls) != 0

        # 从管理器中获取一个新的待爬取的url

    def get_new_url(self):
        new_url = self.rm.getSetsOneDel(self.new_urls)
        self.rm.setSets(self.old_urls, new_url)
        return new_url

        # 从管理器中获取所有的待爬取的url

    def get_new_urls(self):
        new_urls = self.rm.getSetsListDel(self.new_urls)
        for new_url in new_urls:
            self.rm.setSets(self.old_urls, new_url)
        return new_urls
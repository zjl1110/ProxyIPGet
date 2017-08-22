# -*- coding: utf-8 -*-
#__author__="ZJL"

from common.redis_manager import RedisManager as rm


# Html页面管理器
class HtmlManager(object):
    def __init__(self, new_htmls="new_htmls", **key):
        self.rm = rm()
        self.new_htmls = new_htmls

        # 向管理器中添加一个新的html

    def add_new_html(self, html):
        if html is None:
            return
            # 如果不在队列中就添加新html
        if not self.rm.isExist(self.new_htmls, html):
            self.rm.setSets(self.new_htmls, html)

            # 向管理器中添加新的更多的html

    def add_new_htmls(self, htmls):
        if htmls is None or len(htmls) == 0:
            return
        for html in htmls:
            self.add_new_html(html)

            # 判断管理器是否有新的html

    def has_new_html(self):
        return self.rm.setsLen(self.new_htmls) != 0

        # 从管理器中获取一个html

    def get_new_html(self):
        new_html = self.rm.getSetsOneDel(self.new_htmls)
        return new_html
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-03 21:44:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from urlmanage import *
from storedate import *
from htmldownload import Download
from parse import htparse
class spiderman(object):
    def __init__(self):
        self.manage = urlmanage()
        self.dl = Download()
        self.sd = storedate()
        self.parse = htparse()

    def crawl(self,url):
        self.manage.new_urls_add(url)
        self.sd.write_head(self.sd.filepath)
        while (self.manage.has_new_url() and self.manage.old_urls_size()<3000):
            try:
                new_url = self.manage.get_new_url()
                print(new_url)
                html = self.dl.download(new_url)
                print(html)
                new_urls,date = self.parse.par(new_url,html)
                print(new_urls,date)
                for new_url in new_urls:
                    self.manage.new_urls_add(new_url)
                    self.sd.Sd(date)
                    print("已经抓取了%s个链接"%self.manage.old_urls_size())
                    self.sd.write_html(self.sd.filepath)
            except Exception as e:
                print("........................................失败原因:%s"%e)
                self.manage.save_progress('new_urls.txt',self.manage.new_urls())
                self.manage.load_progress('old_urls.txt',self.manage.old_urls())
        self.sd.write_end(self.sd.filepath)
        print(self.manage.new_urls_size())

if __name__ == '__main__':
    sman = spiderman()
    sman.crawl("https://baike.baidu.com/item/NO%20GAME%20NO%20LIFE%20%E6%B8%B8%E6%88%8F%E4%BA%BA%E7%94%9F/3490145?fromtitle=no%20game%20no%20life&fromid=18528516")

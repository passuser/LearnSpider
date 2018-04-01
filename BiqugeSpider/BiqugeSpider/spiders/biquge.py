#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#Date     :2018-04-01 17:06:15
#Author   : by DMH
#relate on:主要是爬取笔趣阁的小说章节目录、链接及相关信息，使用scrapy框架爬取，mongodb储存数据。
#                                                                                                                                 
###############################################################################################################################################
import scrapy,urllib
class Biquge(scrapy.Spider):
    name = 'binovel'
    start_urls = ['http://www.biquge.com.tw/']

    def parse(self,response):
        rurl = 'http://www.biquge.com.tw/'
        novellist = response.xpath('/html/body//div[@id="newscontent"]//a')
        for href in novellist:
            novelurl = href.xpath('./@href').extract()[0]
            if 'html' in novelurl:
                pass
            else:
                yield scrapy.Request(url=novelurl,callback=self.parse_novel)
        noveltypes = response.xpath('//div[@class="nav"]//li[position()>1]/a')
        for noveltype in noveltypes:
            noveltype = urllib.parse.urljoin(rurl,noveltype.xpath('./@href').extract()[0])
            yield scrapy.Request(url=noveltype,callback=self.parse)

    def parse_novel(self,response):
        pass

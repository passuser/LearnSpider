#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#Date     :2018-04-01 17:06:15
#Author   : by DMH
#relate on:主要是爬取笔趣阁的小说章节目录、链接及相关信息，使用scrapy框架爬取，mongodb储存数据。
#                                                                                                                                 
###############################################################################################################################################
import scrapy,urllib
from BiqugeSpider.items import BiqugespiderItem  
class Biquge(scrapy.Spider):
    name = 'binovel'
    start_urls = ['http://www.biquge.com.tw/']

    def __init__(self):
        self.crawledurl = set()
        self.rooturl = 'http://www.biquge.com.tw/'

    def parse(self,response):
        novellist = response.xpath('/html//div[@id="main"]//a')
        for href in novellist:
            novelurl = href.xpath('./@href').extract()[0]
            if 'html' in novelurl or novelurl in self.crawledurl:
                pass
            else:
                self.crawledurl.add(novelurl)
                yield scrapy.Request(url=novelurl,callback=self.parse_novel)
        noveltypes = response.xpath('//div[@class="nav"]//li[position()>1]/a')
        for noveltype in noveltypes:
            noveltype = urllib.parse.urljoin(self.rooturl,noveltype.xpath('./@href').extract()[0])
            yield scrapy.Request(url=noveltype,callback=self.parse)

    def parse_novel(self,response):
        novelname = response.xpath('/html//div[@id="info"]/h1/text()').extract()[0]
        novelauthor = response.xpath('/html//div[@id="info"]/p[1]/text()').extract()[0].split('：')[-1]
        novelcontext = []
        a = response.xpath('/html//div[@id="list"]//dd/a')
        for p in a:
            title = p.xpath('./text()').extract()[0]
            link = urllib.parse.urljoin(self.rooturl,p.xpath('./@href').extract()[0])
            chapter = {'章节':title,'链接':link}
            novelcontext.append({'章节':title,'链接':link})
        item = BiqugespiderItem(novelname=novelname,novelauthor=novelauthor,novelchapter=novelcontext)
        yield item

#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:ToutiaoSpider.py
#Created Time:2018-08-05
#################################################
'''
今日头条街拍爬虫，爬取街拍图。使用SCRAPY框架开发，将图片按指定路径储存。
:root_url:https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D
:url:https://www.toutiao.com/search_content/
:parmas:{'offset': '0',:每次增加20到120
 'format': 'json',
 'keyword': '街拍',
 'autoload': 'true',
 'count': '20',
 'cur_tab': '1',
 'from': 'search_tab'}
:start_header:{'Host': 'www.toutiao.com',
 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Accept-Language': 'en-US,en;q=0.5',
 'Accept-Encoding': 'gzip, deflate',
 'Connection': 'keep-alive',
 'Upgrade-Insecure-Requests': '1',
 'DNT': '1',
 'Pragma': 'no-cache',
 'Cache-Control': 'no-cache'}
 :update:{'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
 'X-Request-with': 'XMLHttpRequest'
 }
 重定向url为/groupxxxxxxxxxxxx /axxxxxxxx
'''
import scrapy 
class toutiao_spider(scrapy.Spider):
    name='Toutiao'
    allow=['toutiao']
    start_urls=['https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D']

    def parse(self,response):
        pass

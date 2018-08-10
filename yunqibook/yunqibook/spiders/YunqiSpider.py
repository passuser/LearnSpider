#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:YunqiSpider.py
#Created Time:2018-08-07
#################################################
'''
爬云起书院的小说，采用scrapy开发，提取数据以mongodb储存，scrapy-redis去重

'''
import scrapy 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from yunqibook.items import YunqibookItemList,YunqibookItemDetail 

class YunqiSpider(CrawlSpider):
    
    name = 'yunqi.qq.com'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n30p1']
    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self,response):
        books = response.xpath(".//div[@class='book']")
        for book in books:
            book_image = book.xpath("./a/img/@src").extract_first()  
            book_name =  book.xpath("./div[@class='book_info']/h3/a/text()").extract_first()
            bookinfos = book.xpath("./div[@class='book_info']//dd")
            bookurl = book.xpath("./div[@class='book_info']/h3/a/@herf").extract_first()
            bookid = book.xpath("./div[@class='book_info']/h3/a/@id").extract_first()
            if len(bookinfos) > 5 :
                book_author =  bookinfos[0].xpath("./a/text()").extract_first()
                book_updaetime =  bookinfos[3].xpath("./text()").extract_first()
                book_info =  bookinfos[5].xpath("./text()").extract_first()
                book_type =  bookinfos[1].xpath("./a/text()").extract_first().lstrip('[').rstrip(']')
                book_words = int(bookinfos[4].xpath("./text()").extract_first())
                book_status =  bookinfos[2].xpath("./text()").extract_first()
            else:
                book_author =  ''
                book_updaetime = ''  
                book_info =  ''
                book_type =  ''
                book_words = 0
                book_status = ''
            List_items = YunqibookItemList(
                book_image=book_image,book_name=book_name,bookurl=bookurl,
                book_author=book_author,book_updaetime=book_updaetime,book_info=book_info,book_type=book_info,
                book_words=book_words,book_status=book_status)
            yield List_items 
            from scrapy.shell import inspect_response 
            inspect_response(response)
            request = scrapy.Request(url=bookurl,callback=self.parse_book_detail)
            request.meta['bookid'] = bookid 
            yield request

    def parse_book_detail(self,response):
        bookdetail = response.xapth(".//div[@id='novelInfo']/table//tr")
        if bookdetail :
            book_click = bookdetail[1].xpath("./td/text()").extract()[0]
            book_clickMonth = bookdetail[2].xpath("./td/text()").extract()[0]
            book_clickWeek = bookdetail[3].xpath("./td/text()").extract()[0]
            book_people = bookdetail[1].xpath("./td/text()").extract()[1]
            book_peopleMonth = bookdetail[2].xpath("./td/text()").extract()[1]
            book_peopleWeek = bookdetail[3].xpath("./td/text()").extract()[1]
            book_comment = int(bookdetail[4].xpath("./td/span/text()").extract_first())
            book_recomm =bookdetail[1].xpath("./td/text()").extract()[2]
            book_recommMonth =bookdetail[2].xpath("./td/text()").extract()[2]
            book_recommWeek =bookdetail[3].xpath("./td/text()").extract()[2]
        Detailitems = YunqibookItemDetail(
            book_click=book_click,book_clickMonth=book_clickMonth,book_clickWeek=book_clickWeek,
            book_people=book_people,book_peopleWeek=book_peopleWeek,book_peopleMonth=book_peopleMonth,book_recomm=book_recomm,
            book_recommWeek=book_recommWeek,book_recommMonth=book_recommMonth,book_comment=book_comment)
        yield Detailitems 


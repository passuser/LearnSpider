# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YunqibookItemList(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_image = scrapy.Field()
    bookurl = scrapy.Field()
    bookid = scrapy.Field()
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_updaetime = scrapy.Field()
    book_info = scrapy.Field()
    book_type = scrapy.Field()
    book_words = scrapy.Field()
    book_status = scrapy.Field()

class YunqibookItemDetail(scrapy.Item):
    bookid = scrapy.Field()
    book_click = scrapy.Field()
    book_clickMonth = scrapy.Field()
    book_clickWeek = scrapy.Field()
    book_people = scrapy.Field()
    book_peopleMonth = scrapy.Field()
    book_peopleWeek = scrapy.Field()
    book_comment = scrapy.Field()
    book_recomm =scrapy.Field()
    book_recommMonth =scrapy.Field()
    book_recommWeek =scrapy.Field()

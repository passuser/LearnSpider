# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class LearnScrapyItem(scrapy.Item):
    novelname = scrapy.Field()
    novelauthor = scrapy.Field()
    novelcontext = scrapy.Field()
    



# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class LearnScrapyPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient().novel

    def process_item(self, item, spider):
        self.db = self.client['biqu']
        self.db.insert(dict(item))
        print('write')
        return item

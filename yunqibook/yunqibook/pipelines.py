# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo 
class YunqibookPipeline(object):
    def __init__(self,mongo_url,mongo_db,replicaset):
        self.mongo_url = mongo_url 
        self.mongo_db = mongo_db 
        self.replicaset = replicaset

    @classmethod 
    def from_crawler(cls,crawler):
        return cls(
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DATABASE','spider'),
            replicaset = crawler.settings.get('REPLICASET')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url,replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,List_items):
            self._process_booklist_item(item)
        else:
            self._process_bookdetail_item(item)
        return item

    def _process_booklist_item(self,item):
        self.db.bookinfo.insert(dict(item))

    def _process_bookdetail_item(self,item):
        '''
        数据清洗
        '''
        item['book_click'] = item['book_click'].split('：')[1]
        item['book_clickMonth'] = item['book_clickMonth'].split('：')[1]
        item['book_clickWeek'] = item['book_clickWeek'].split('：')[1]
        item['book_people'] = item['book_people'].split('：')[1]
        item['book_peopleMonth'] = item['book_peopleMonth'].split('：')[1]
        item['book_peopleWeek'] = item['book_peopleWeek'].split('：')[1]
        item['book_recomm'] =item['book_recomm'].split('：')[1]
        item['book_recommMonth'] = item['book_recommMonth'].split('：')[1]
        item['book_recommWeek'] = item['book_recommWeek'].split('：')[1]
        self.db.bookhot.insert(dict(item))

    

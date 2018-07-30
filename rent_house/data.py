#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#################################################
'''
数据存储处理查询模块
'''
import pymongo
class Database(object):
    def __init__(self):
        self.client=pymongo.MongoClient('mongodb://localhost:27017')
        self.db=self.client.spider

    def insert(self,house):
        self.db.houses.insert(house)



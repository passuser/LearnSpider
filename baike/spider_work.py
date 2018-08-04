#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:spider_work.py
#Created Time:2018-08-04
#################################################
import queue,time
from urlmanage import *
from htmldownload import Download
from parse import htparse
from multiprocessing.managers import BaseManager
from multiprocessing import Process
'''
:param url_q:将url从urlmanage传递到爬虫节点
:param result_q: 爬虫节点将数据返回给数据提取
:param conn_q:数据提取将url提交到urlmanage
:param store_q:从数据提取传到数据储存
'''
class spider_work(object):
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        server_addr='127.0.0.1'
        print('Connecting to server %s...'%server_addr)
        self.m=BaseManager(address=(server_addr,8050),authkey=b'baidubaike')
        self.m.connect()
        self.url_down=self.m.get_task_queue()
        self.result=self.m.get_result_queue()
        self.dl=Download()
        self.pr=htparse()
        print('init finish!')

    def crawl(self):
        while True:
            try:
                if not self.url_down.empty():
                    print('节点开始工作...')
                    url=self.url_down.get()
                    if url == 'stop':
                        print('节点正在停止工作...')
                        self.result.put({'new_urls':'stop','data':'stop'})
                        print("通知其他进程停止工作...")
                        return 
                    print('节点正在解析：%s....'%url.encode('utf-8'))
                    html=self.dl.download(url)
                    new_urls,data=self.pr.par(url,html)
                    print(data)
                    self.result.put({'new_urls':new_urls,'data':data})
            except EOFError as e:
                print('连接失败...')
            except Exception as e:
                print('失败原因:%s'%e)

if __name__=='__main__':
    spider=spider_work()
    spider.crawl()

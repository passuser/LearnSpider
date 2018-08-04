#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:spider_service.py
#Created Time:2018-08-03
#################################################
import queue,time
from urlmanage import *
from storedate import *
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
class spider_manage(object):
    def __init__(self):
        pass 

    def start_manger(self,url_q,result_q):
        BaseManager.register('get_url_queue',callable=lambda: url_q)
        BaseManager.register('get_result_queue',callable=lambda: result_q)
        Man=BaseManager(address=('127.0.0.1',5000),authkey='baidubaike'.encode('utf-8'))
        return Man 

    def urlmanage_proc(self,url_q,conn_q,store_q,root_url):
        ul=urlmanage()
        ul.new_url_add(root_url)
        while True:
            while ul.has_new_url() :
                new_url=ul.get_new_url()
                url_q.put(new_url)
                print(new_url)
                print('已爬取%d个链接'%ul.old_urls_size())
                print(ul.old_urls)
                if ul.old_urls_size() > 30:
                    url_q.put('stop')
                    print('爬取结束，各节点开始停止工作！')
                    ul.save_progress('new_urls.txt',ul.new_urls)
                    ul.load_progress('old_urls.txt',ul.old_urls)
                    return None 
                try :
                    if not conn_q.empty():
                        urls=conn_q.get()
                        ul.new_urls_add(urls)
                except Exception as e:
                    time.sleep(0.41)
        
    def result_proc(self,result_q,conn_q,store_q):
        while True:
            try:
                if not result_q.empty():
                    content=result_q.get(True)
                    if content['new_urls']=='stop' :
                        store_q.put('stop')
                    conn_q.put(content['new_urls'])
                    store_q.put(content['data'])
                else:
                    time.sleep(0.11)
            except Exception as e:
                time.sleep(0.31)
                print(e)

    def store_proc(self,store_q):
        sd=storedate()
        while True:
            if not store_q.empty():
                data=store_q.get()
                print(data)
                if data=='stop':
                    print('停止储存中')
                sd.write_html(data)
            else:
                time.sleep(0.21)

if __name__=='__main__':
    url_q=queue.Queue()
    result_q=queue.Queue()
    store_q=queue.Queue()
    conn_q=queue.Queue()
    sman=spider_manage()
    manage=sman.start_manger(url_q,result_q)
    ul_proc=Process(target=sman.urlmanage_proc,args=(url_q,conn_q,store_q,'https://baike.baidu.com/item/NO%20GAME%20NO%20LIFE%20%E6%B8%B8%E6%88%8F%E4%BA%BA%E7%94%9F/3490145?fromtitle=no%20game%20no%20life&fromid=18528516',))
    re_proc=Process(target=sman.result_proc,args=(result_q,conn_q,store_q,))
    sd_proc=Process(target=sman.store_proc,args=(store_q,))
    ul_proc.start()
    re_proc.start()
    sd_proc.start()
    manage.get_server().serve_forever()

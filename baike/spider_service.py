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
:param url_qe:将url从urlmanage传递到爬虫节点
:param result_q: 爬虫节点将数据返回给数据提取
:param conn_q:数据提取将url提交到urlmanage
:param store_q:从数据提取传到数据储存
'''
class spider_manage(object):
    def __init__(self):
        self.manage=urlmanage()
        self.sd=storedate()

    def start_manger(self,url_qe,result_q):
        BaseManager.register('get_task_queue',callable=lambda: url_qe)
        BaseManager.register('get_result_queue',callable=lambda: result_q)
        Man=BaseManager(address=('',8050),authkey=b'baidubaike')
        return Man 

    def urlmanage_proc(self,url_qe,conn_q,store_q,root_url):
        self.manage.new_urls.add(root_url)
        while True:
            while self.manage.has_new_url() :
                new_url=self.manage.get_new_url()
                url_qe.put(new_url)
                print('已爬取第%d个链接,地址为%s'%(self.manage.old_urls_size(),new_url))
                if self.manage.old_urls_size() > 3000:
                    url_qe.put('stop')
                    print('爬取结束，各节点开始停止工作！')
                    ul.save_progress('new_urls.txt',self.manage.new_urls)
                    ul.load_progress('old_urls.txt',self.manage.old_urls)
                    return None 
                try :
                    if not conn_q.empty():
                        urls=conn_q.get()
                        self.manage.new_urls_add(urls)
                except Exception as e:
                    time.sleep(0.1)
        
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
                    time.sleep(0.1)
            except Exception as e:
                time.sleep(0.1)
                print(e)

    def store_proc(self,store_q):
        while True:
            if not store_q.empty():
                data=store_q.get()
                print(data)
                if data=='stop':
                    print('停止储存中')
                self.sd.write_html(data)
            else:
                time.sleep(0.1)

if __name__=='__main__':
    url_qe=queue.Queue()
    result_q=queue.Queue()
    store_q=queue.Queue()
    conn_q=queue.Queue()
    sman=spider_manage()
    manage=sman.start_manger(url_qe,result_q)
    ul_proc=Process(target=sman.urlmanage_proc,args=(url_qe,conn_q,store_q,'https://baike.baidu.com/item/NO%20GAME%20NO%20LIFE%20%E6%B8%B8%E6%88%8F%E4%BA%BA%E7%94%9F/3490145?fromtitle=no%20game%20no%20life&fromid=18528516',))
    re_proc=Process(target=sman.result_proc,args=(result_q,conn_q,store_q,))
    sd_proc=Process(target=sman.store_proc,args=(store_q,))
    ul_proc.start()
    re_proc.start()
    sd_proc.start()
    manage.get_server().serve_forever()

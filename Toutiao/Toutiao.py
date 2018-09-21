#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:Toutiao.py
#Created Time:2018-09-16
#################################################
'''
https://www.toutiao.com/search_content/?offset=0&format=json&keyword=街拍&autoload=true&count=20&cur_tab=3&from=gallery
offset最大为140，每次递增20。
'''
from parse import parse 
from download import download 
from save import save 
import pickle,os 
import threading
from gevent.pool import Pool 
class spider(object):
    def __init__(self):
        self.parse = parse()
        self.dl = download()
        self.save = save()
        self.nowpath = os.getcwd()
        self.pool = Pool(10)
        self.old_group = self.load_set('old.txt') if os.path.exists('old.txt') else set()
        self.new_group = self.load_set('new.txt') if os.path.exists('new.txt') else set()
        self.max_set = int(input('请输入下载图片张数：'))
    
    def group_dl(self,g_list):
        new_group_list = [g for g in g_list if g not in self.old_group]
        for new_group in new_group_list:
            self.old_group.add(new_group)
        results = self.pool.map(self.dl.html_down,new_group_list)
        return results 

    def imgset_dl(self,img_urls):
        image_list = self.pool.map(self.dl.img_down,img_urls)
        return image_list 
    
    def save_set(self,filename,collection):
        if collection:
            with open(self.nowpath + '/'+filename,'wb') as f:
                pickle.dump(collection,f)
                print('保存成功%s'%self.nowpath+'/'+filename)

    def load_set(self,filename):
        with open(self.nowpath+'/'+filename,'rb') as f:
            return pickle.load(f)
            print('加载进度文件成功！')

    def main_run(self,offset):
        json_data = self.dl.html_down(u'https://www.toutiao.com/search_content/?offset=%s&format=json&keyword=街拍&autoload=true&count=20&cur_tab=3&from=gallery'%offset)
        while True:
            if json_data:
                g_list = self.parse.json_parse(json_data)
                reponse = self.group_dl(g_list)
                for r in reponse:
                    title,img_urls,remmend_urls = self.parse.html_parse(r.text)
                    for ren in remmend_urls:
                        if ren not in self.old_group and ren not in self.new_group:
                            self.new_group.add(ren)
                    image_list = self.imgset_dl(img_urls)
                    for img in image_list:
                        if self.save.i < self.max_set:
                            self.save.img_save(img,title)
                        else:
                            print('达到下载数量,开始退出！')
                            break
                    if self.save.i > self.max_set:
                        break
                if self.save.i > self.max_set:
                    break
                    
                json_data = None
            k = self.new_group.pop()
            if k not in self.old_group:
                r = self.dl.html_down(k)
                self.old_group.add(k)

                title,img_urls,re_list = self.parse.html_parse(r.text)
                for ren in re_list:
                    if ren not in self.old_group and ren not in self.new_group:
                        self.new_group.add(ren)
                image_list = self.imgset_dl(img_urls)
                for img in image_list:
                    if self.save.i <= self.max_set:
                        self.save.img_save(img,title)
                    else:
                        print('达到下载数量,开始退出！')
                        break
                if self.save.i > self.max_set:
                    break

    def process_run(self,arg):
        t = threading.Thread(target=self.main_run,args=(arg,))
        t.start()
        t.join()


#   s.save_set('old.txt',s.old_group)
#   s.save_set('new.txt',s.new_group)

if __name__ == '__main__':
    s = spider()
    offset = 0
    try:
        list(map(s.process_run,[offset+n*20 for n in range(8)]))

    except Exception as e:
        print('出现错误：%s\n开始保存进度文件'%e)
        s.save_set('old.txt',s.old_group)
        s.save_set('new.txt',s.new_group)
    s.save_set('old.txt',s.old_group)
    s.save_set('new.txt',s.new_group)
    print('------------------------------------结束--------------------------------------')

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
class spider(object):
    def __init__(self):
        self.parse = parse()
        self.dl = download()
        self.save = save()
        self.nowpath = os.getcwd()
        self.old_group = self.load_set('old.txt') if os.path.exists('old.txt') else set()
        self.new_group = self.load_set('new.txt') if os.path.exists('new.txt') else set()
    
    def group_dl(self,group_list):
        for g in g_list:
            if g not in s.old_group:
                response = s.dl.html_down(g[1])
                s.old_group.add(g)
                yield response,g[0]  

    def imgset_dl(self,img_urls,title):
            for img_url in img_urls:
                img = s.dl.img_down(img_url)
                if img:
                    s.save.img_save(img.content,title)
    
    def save_set(self,filename,collection):
        if collection:
            with open(self.nowpath + '/'+filename,'wb') as f:
                pickle.dump(collection,f)
                print('保存成功%s'%self.nowpath+'/'+filename)

    def load_set(self,filename):
        with open(self.nowpath+'/'+filename,'rb') as f:
            return pickle.load(f)
            print('加载进度文件成功！')


if __name__ == '__main__':
    s = spider()
    offset = 0
    max_set = int(input('请输入下载图片张数：'))
    try:
        while s.save.i < max_set:
            if offset <= 140:
                json_data = s.dl.html_down(u'https://www.toutiao.com/search_content/?offset=%s&format=json&keyword=街拍&autoload=true&count=20&cur_tab=3&from=gallery'%offset)
                offset = offset + 20
                g_list = s.parse.json_parse(json_data)
                reponse = s.group_dl(g_list)
                for r,title in reponse:
                    re_list = s.parse.recom_parse(r.text)
                    for ren in re_list:
                        if ren not in s.old_group:
                            s.new_group.add(ren)
                    img_urls = s.parse.html_parse(r.text)
                    s.imgset_dl(img_urls,title)
            else:
                k = s.new_group.pop()
                if k not in s.old_group:
                    r = s.dl.html_down(k[1])
                    s.old_group.add(k)
                    img_urls = s.parse.html_parse(r.text)
                    s.imgset_dl(img_urls,k[0])

    except Exception as e:
        print('出现错误：%s\n开始保存进度文件'%e)
        s.save_set('old.txt',s.old_group)
        s.save_set('new.txt',s.new_group)

    s.save_set('old.txt',s.old_group)
    s.save_set('new.txt',s.new_group)
    print('------------------------------------结束--------------------------------------')

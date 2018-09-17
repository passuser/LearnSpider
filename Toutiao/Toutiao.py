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
class spider(object):
    def __init__(self):
        self.parse = parse()
        self.dl = download()
        self.save = save()

if __name__ == '__main__':
    s = spider()
    max_set,offset = 140,0
    while offset < max_set:
        json_data = s.dl.html_down(u'https://www.toutiao.com/search_content/?offset=%s&format=json&keyword=街拍&autoload=true&count=20&cur_tab=3&from=gallery'%offset)
        offset = offset + 20
        try:
            g_list = s.parse.json_parse(json_data)
            for g in g_list:
                r = s.dl.html_down(g[1])
                img_urls = s.parse.html_parse(r.text)
                for img_url in img_urls:
                    img = s.dl.img_down(img_url)
                    s.save.img_save(img.content,g[0])
        except Exception as e:
            print('出现错误：%s'%e)
    print('------------------------------------结束--------------------------------------')

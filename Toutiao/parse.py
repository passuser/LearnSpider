#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:parse.py
#Created Time:2018-09-16
#################################################
'''
解析模块：解析json数据、从网页中获取json
'''
import json,re
from lxml import etree
class parse(object):
    def __init__(self):
        pass 

    def json_parse(self,html):
        datas = html.json()['data']
        group = {}
        groups = []
        for data in datas:
            group['title'],group['source'],group['img_set'] = data['title'],data['source'],data['article_url']
            groups.append(group)
        return groups 

    def html_parse(self,html):
        js_patern = re.compile('JSON\.parse\(\"(.*)\"\),')
        js = re.search(js_patern,html).group(1)
        js = js.replace('\\','')
        url_patern = re.compile(r'"uri":"(\S+?)"')
        urls = re.findall(url_patern,js)
        urls = ['http://pb3.pstatp.com/'+url for url in urls]
        return urls 

    def recom_parse(self,html):
        '''
        相关推荐
        '''
        pass 


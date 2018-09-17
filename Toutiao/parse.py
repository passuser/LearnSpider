#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:parse.py
#Created Time:2018-09-16
#################################################
'''
解析模块：解析json数据、从网页中获取json
'''
import re
class parse(object):
    def __init__(self):
        pass 

    def json_parse(self,html):
        datas = html.json()['data']
        '''
        l,item = [],{}
        for datae in datas:
            item['title'] = datae['title']
            item['img_set'] = datae['article_url']
            l.append(item)
        return l
    使用这段代码时，会重复某个数据
        '''
        titles = [item['title'] for item in datas]
        img_set = [item['article_url'] for item in datas] 
        return list(zip(titles,img_set))

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
        recomm_p = re.compile(r'iblingList:\s(\S+),')
        title_p = re.compile(r'"title":"(\S+?)"')
        urls_p = re.compile(r'"source_url":"(\S+?)"')
        recomm = re.search(recomm_p,html).group(1)
        titles = re.findall(title_p,recomm)
        urls = re.findall(urls_p,recomm)
        return list(zip(titles,urls))

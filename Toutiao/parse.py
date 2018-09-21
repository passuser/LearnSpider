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
        img_set = [item['article_url'] for item in datas] 
        return img_set

    def html_parse(self,html):
        '''
        详细页面负责解析标题、图片下载链接、相关推荐
        '''
        js_patern = re.compile('JSON\.parse\(\"(.*)\"\),')   #获取本页的图片链接
        js = re.search(js_patern,html).group(1)
        js = js.replace('\\','')

        img_url_patern = re.compile(r'"uri":"(\S+?)"')
        title_p = re.compile(r'(?<=<(title)>)\S*(?=</\1)')
        recommend_p = re.compile(r'iblingList:\s(\S+),')
        recommend_urls_p = re.compile(r'"source_url":"(\S+?)"') #正则表达式

#        titles_p = re.compile(r'"title":"(\S+?)"')

        recomm = re.search(recommend_p,html).group(1)
        title = re.search(title_p,html).group()
        urls = re.findall(img_url_patern,js)
        img_urls = ['http://pb3.pstatp.com/'+url for url in urls] #图集的链接
        recommend_urls = re.findall(recommend_urls_p,recomm)
        return title,img_urls,recommend_urls 


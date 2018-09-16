#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:dowmload.py
#Created Time:2018-09-16
#################################################
'''
下载模块：负责下载网页、图片
'''
import requests,json 
class download(object):
    def __init__(self):
        with open('headers.txt','r') as f:
            self.header = json.load(f)

    def html_down(self,url):
        if url:
            html = requests.get(url,headers=self.header)
            if html.status_code == 200:
                return html 

    def img_down(self,img_url):
        if img_url:
            img = requests.get(img_url,allow_redirect=False)
            if img.status_code == 200:
                return img 




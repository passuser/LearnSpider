#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-
import requests 
import chardet
class html_down(object):
    def __init__(self):
        self.headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept':'text/html',
            'Accept-Encoding':'gzip, deflate',
            'Pragma':'no-cache',
            'Referer': 'http://www.58.com/',
            'Cache-Control':'no-cache'
        }
        self.proixy={}

    def down(self,url):
        response=requests.Session().get(url,headers=self.headers)
        if responise.status_code==200:
            responise.encoding=chardet.detect(respone.content)['encoding']
            return respone.text 
        else:
            pass 


#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#Date     :2018-04-02 18:36:14
#Author   : by DMH
#relate on:爬笔趣阁小说。
#                                                                                                                                 
###############################################################################################################################################
import urllib,requests,chardet,json
from bs4 import BeautifulSoup
from lxml import etree
class biquge(object):
    def __init__(self):
        self.crawled_url = set()
        self.i = 0

    def html_response(self,url):
   #     proxy = {
   #         'http':'http://127.0.0.1:1159',
   #         'https':'http://127.0.0.1:1159'
   #         }
        r = requests.get(url)
        r.encoding=chardet.detect(r.content)['encoding']
        if r.status_code == 200:
            return r.text,url 
        else:
            return None

    def parse(self,html,reurl):
        soup = BeautifulSoup(html,'lxml')
        novels = soup.find('div',id='main').find_all('a')
        i=0
        for novel in novels:
            novel = novel.get('href')
            if 'html' in novel or novel in self.crawled_url:
                pass
            else:
                self.crawled_url.add(novel)
                self.i+=1
                html,novel = self.html_response(novel)
                data = self.parse_novel(html,novel)
                print('爬取的第%d本小说名：%s'%(self.i,data['小说']))
                with open('biquge','a') as f:
                    p=json.dump(data,ensure_ascii=False,indent=4,fp=f)
                    # p=pickle.dump(data,file=f)
        for typ in soup.find('div',class_='nav').find_all('a'):
            tyurl = urllib.parse.urljoin(reurl,typ.get('href'))
            if tyurl not in self.crawled_url:
                self.crawled_url.add(tyurl)
                html,tyurl = self.html_response(tyurl)
                self.parse(html,tyurl)
            else:
                pass


    def parse_novel(self,html,url):
        soup = BeautifulSoup(html,'lxml')
        novel = soup.find('div',id='info')
        name = novel.find('h1').string
        author = novel.find('p').string.split('：')[-1]
        chapters = soup.find('div',id='list').find_all('a') 
        content=[]
        i = 0
        for chap in chapters:
            link = urllib.parse.urljoin(url,chap.get('href'))
            title = chap.string
            content.append({'章节':title,'网址':link})
            i+=1
        print('已抓取%d章节目录'%i,end='\t')
        data = {'小说':name,'作者':author,'章节':content}
        return data 

if __name__=='__main__':
    b = biquge()
    html,url= b.html_response("http://www.biquge.com.tw")
    b.parse(html,url)

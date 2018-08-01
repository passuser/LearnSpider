#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#################################################
'''
查询租房信息
''' 
import time
from bs4 import BeautifulSoup
from lxml import etree
from data import Database 
from download import html_down 
from parse import parse 

class manag(object):
    def __init__(self):
        self.db=Database()
        self.dl=html_down()
        self.pr=parse()

if __name__=='__main__':
    Spider=manag()
    url='http://www.58.com/changecity/'
    html=Spider.dl.down(url)
    soup=BeautifulSoup(html,'lxml')
    city_url=None
    while city_url==None:
        city=input('请输入城市名（如果再次出现，说明该城市无法查询）：\n')
        for a in soup.find_all('a'):
            if city == a.string:
                city_url='http:'+a.get('href')+'chuzu'
        html=Spider.dl.down(city_url)
        next_pag,house_list=Spider.pr.parse_html(html)
        i=0
        while next_pag:
            for house_url in house_list:
                if i % 10 ==0:
                    time.sleep(0.5)
                try:
                    house_html=Spider.dl.down('http:'+house_url)
                    house=Spider.pr.Parse_html(house_html)
                    i=i+1
                    print(i,house)
                    Spider.db.insert(house)
                except  IndexError as e:
                    print(e,house_html)
                    time.sleep(1)
                    continue 
                except Exception as e:
                    print('.................................................................................................................................................................................')
                    print(e,house_html)
                    print('.................................................................................................................................................................................')
                    continue
            next_pag,house_list=Spider.pr.parse_html(html)
    print('数据爬取结束')


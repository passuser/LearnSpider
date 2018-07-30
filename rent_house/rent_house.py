#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#################################################
'''
查询租房信息
'''
import requests,chardet,re,time 
from bs4 import BeautifulSoup
from lxml import etree 
headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept':'text/html',
    'Accept-Encoding':'gzip, deflate',
    'Pragma':'no-cache',
    'Referer': 'http://www.58.com/',
    'Cache-Control':'no-cache'
}
url='http://www.58.com/changecity/'
r=requests.Session().get(url,headers=headers)
r.encoding=chardet.detect(r.content)['encoding']
soup=BeautifulSoup(r.text,'lxml')
city_url=None
while city_url==None:
    city=input('请输入城市名（如果再次出现，说明该城市无法查询）：\n')
    for a in soup.find_all('a'):
        if city == a.string:
            city_url=a.get('href')+'chuzu'
r=requests.Session().get(city_url,headers=headers)
r.encoding=chardet.detect(r.content)['encoding']
soup=BeautifulSoup(r.text,'lxml')
soup.find('a',class_='next').get('href')   "下页 "
for a_url in soup.select('h2'):
    pass  "抓取信息页，IP过于频繁访问会要求滑动验证，更换IP "
    house_soup=BeautifulSoup(house_pag.text,'lxml')
    info=k_soup.find('ul',class_='f14')
    rent=house_soup.b.string 
    rent_to_pay=house_soup.select('span.c_333')[0].string 
    rent_house=info.find_all('span',class_='')[0]
    house_type=str(info.find_all('span',class_='')[1].string)spilt()[0]
    house_area=str(info.find_all('span',class_='')[1].string)spilt()[1]
    towards=str(info.find_all('span',class_='')[2].string)spilt()[0]
    layout=str(info.find_all('span',class_='')[2].string)spilt()[1]
    town=info.find_all('span',class_="")[3].string 
    zone=info.find_all('a',class_='c_333 ah')[1].string 
    address=info.select('span.dz')[0].string.strip()
    call=house_soup.select('span.house-chat-txt')[0].string 
    agent=house_soup.find('a',class_='c_000').string
    rent_conditions=''
    for span in house_soup.find_all('span',class_='a2')[-1].select('span'):
        rent_conditions=rent_conditions+str(span.string)


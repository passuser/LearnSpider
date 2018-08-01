#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#################################################
import re 
from bs4 import BeautifulSoup
from lxml import etree 

class parse(object):
    def __init__(self):
        pass 

    def parse_html(self,html):
        soup=BeautifulSoup(html,'lxml')
        next_url=soup.find('a',class_='next').get('href')
        house_list=[]
        for url in soup.select('h2'):
            house_list.append(url.a.get('href'))
        return next_url,house_list 

    def Parse_html(self,html):
        house_soup=BeautifulSoup(html,'lxml')
        info=house_soup.find('ul',class_='f14')
        rent=int(house_soup.b.string) 
        rent_to_pay=house_soup.select('span.c_333')[0].string 
        rent_method=info.find_all('span',class_='')[0].string 
        house_type=str(info.find_all('span',class_='')[1].string).split()[0]
        house_area=int(str(info.find_all('span',class_='')[1].string).split()[1])
        towards=str(info.find_all('span',class_='')[2].string).split()[0]
        layout=str(info.find_all('span',class_='')[2].string).split()[1]
        town=info.find_all('span',class_="")[3].string 
        zone=info.find_all('a',class_='c_333 ah')[1].string 
        address=info.select('span.dz')[0].string.strip()
        call=house_soup.select('span.house-chat-txt')[0].string 
        agent=house_soup.find('a',class_='c_000').string
        rent_conditions=''
        for span in house_soup.find_all('span',class_='a2')[-1].select('span'):
            rent_conditions=rent_conditions+str(span.string).strip()
        if rent_conditions=='':
            rent_conditions=house_soup.h1.string
        house={
            'rent':rent,
            'rent_to_pay':rent_to_pay,
            'rent_method':rent_method,
            'house_type':house_type,
            'house_area':house_area,
            'layout':layout,
            'towards':towards,
            'town':town,
            'zone':zone,
            'address':address,
            'call':call,
            'agent':agent,
            'rent_conditions':rent_conditions 
        }
        return house

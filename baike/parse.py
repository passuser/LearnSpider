#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-01 17:42:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from bs4 import BeautifulSoup
import urllib 
import re
from lxml import etree
class htparse(object):
	def par(self,now_url,html_cont):
		soup = BeautifulSoup(html_cont,"lxml")
		new_urls = self._get_new_urls(now_url,soup)
		new_date = self._get_new_date(now_url,soup)
		return new_urls,new_date

	def _get_new_date(self,now_url,soup):
		date = {}
		date['link'] = now_url
		date['item'] = soup.find('dd',class_="lemmaWgt-lemmaTitle-title").find('h1').string
		date['text'] = soup.find('div',class_="lemma-summary").get_text()
		return date
	
	def _get_new_urls(self,now_url,soup):
		new_urls = set()
		links = soup.find('div',class_="lemma-summary").find_all('a',href=re.compile(r'/item/*'))
		for link in links:
			new_url = link['href']
			new_full_url = urllib.parse.urljoin(now_url,new_url)
			new_urls.add(new_full_url)
		return new_urls

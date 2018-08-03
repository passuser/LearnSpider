#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-03 21:33:01
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import time
import codecs
class storedate(object):
	def __init__(self):
		self.dates = []
		self.filepath = 'baike_%s.html'%(time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime()))
		self.write_head(self.filepath)

	def Sd(self,date):
		if date is None:
			return None
		self.dates.append(date)
		if len(self.dates) > 10:
			self.write_html(self.filepath)

	def write_html(self,path):
		fount = codecs.open(path,'a',encoding='utf-8')
		for date in self.dates:
			fount.write("<tr>")
			fount.write("<td>%s</td>"%date['link'])
			fount.write("<td>%s</td>"%date['item'])
			fount.write("<td>%s</td>"%date['text'])
			fount.write("</tr>")
			self.dates.remove(date)
		fount.close()

	def write_head(self,path):
		fount = codecs.open(path,'w',encoding='utf-8')
		fount.write("<html>")
		fount.write("<head><meta charset='utf-8'/></head>")
		fount.write("<body>")
		fount.write("<table>")
		fount.close()

	def write_end(self,path):
		fount = codecs.open(path,'a',encoding='utf-8')
		fount.write("</table>")
		fount.write("</body")
		fount.write("</html>")
		fount.close()

	# def writejson(self,dates):
		# with open('baike2.json','w',encoding='utf-8') as fp:
			# json.dump(dates,fp=fp,indent=4,ensure_ascii=False)

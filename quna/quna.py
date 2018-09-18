#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:quna.py
#Created Time:2018-09-18
#################################################
import codecs
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
'''
使用selenium爬取动态网站
'''

class QunaSpider(object):
    def get_hotel(self,driver, to_city,fromdate,todate):
        print(driver.page_source)
        tocity = driver.find_element_by_name('toCity')
        fromDate = driver.find_element_by_id('fromDate')
        toDate = driver.find_element_by_id('toDate')
        search = driver.find_element_by_class_name('button-search')
        tocity.clear()
        tocity.send_keys(to_city)
        tocity.click()
        fromDate.clear()
        fromDate.send_keys(fromdate)
        toDate.clear()
        toDate.send_keys(todate)
        search.click()
        page_num=0
        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.title_contains(unicode(to_city))
                )
            except Exception as e:
                print(e)
                break
            time.sleep(5)

            js = "window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(js)
            time.sleep(5)

            htm_const = driver.page_source
            soup = BeautifulSoup(htm_const,'html.parser', from_encoding='utf-8')
            infos = soup.find_all(class_="item_hotel_info")
            f = codecs.open(unicode(to_city)+unicode(fromdate)+u'.html', 'a', 'utf-8')
            for info in infos:
                f.write(str(page_num)+'--'*50)
                content = info.get_text().replace(" ","").replace("\t","").strip()
                for line in [ln for ln in content.splitlines() if ln.strip()]:
                    f.write(line)
                    f.write('\n')
            f.close()
            try:
                next_page = WebDriverWait(driver, 10).until(
                EC.visibility_of(driver.find_element_by_css_selector(".item.next"))
                )
                next_page.click()
                page_num+=1
                time.sleep(10)
            except Exception as e:
                print(e)
                break

    def crawl(self,root_url,to_city):
        today = datetime.date.today().strftime('%Y-%m-%d')
        tomorrow=datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')
#         dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS) #设置user-agent
#         dcap['Phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36')
#         driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        driver.maximize_window()
        driver.implicitly_wait(10) 
        self.get_hotel(driver,to_city,today,tomorrow)

if __name__=='__main__':
    spider = QunaSpider()
    city = input('请输入城市名：')
    spider.crawl('https://www.qunar.com/?tab=hotel&ex_track=auto_4e0d874a',city)


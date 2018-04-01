#这个爬虫主要功能是爬取笔趣阁网站的小说章节名和链接及作者名
#使用mongodb储存数据，使用scrapy框架。
import scrapy,re,pymongo
import urllib
from Learn_scrapy.items import LearnScrapyItem 
from scrapy.selector import Selector
class LSpider(scrapy.Spider):
    name = 'novel'
    start_urls = ['http://www.biquge.com.tw/']

    def parse(self,response):
        novels = Selector(response).re(r'href="http://.*\.tw/[0-9]{2}_\d+/"')
        for  novel in novels:
            novel = novel.split('=')[-1].strip('"')
            if novel:
               yield scrapy.Request(url=novel,callback=self.parse_body)
        for k in [s for s in range(8) if s > 1]:
            k = '/html/body//div[@class="nav"]//li[%d]'%k
            url = urllib.parse.urljoin('http://www.biquge.com.tw/',response.xpath(k).xpath('./@href').extract()[0])
            yield scrapy.Request(url=url,callback=self.parse)

    def parse_body(self,response):
        chapcontext=[]
        novelname = response.xpath('/html/body//div[@id="info"]/h1').extract()[0]
        novelauthor = response.xpath('/html//div[@id="info"]/p').extract()[0]
        novelchapters = response.xpath('/html//div[@id="list"]/dl//dd/a')
        for novelchapter in novelchapters:
            chaptername = novelchapter.xpath('./text()').extract()[0]
            chapterlink = novelchapter.xpath('./@href').extract()[0]
            chapcontext.append(['章节',chaptername,'链接',chapterlink])
        item = LearnScrapyItem(novelname=novelname,novelauthor=novelauthor,novelcontext=chapcontext)
        yield item


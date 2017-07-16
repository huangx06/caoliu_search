# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 12:55:53 2017
selenium chrome模拟浏览器爬草榴
@author: huangx06
"""

from selenium import webdriver
import codecs
from mylog import MyLog as mylog

class MovieItem(object):
    movieName = None
    movieNet = None


class GetMovie(object):
	#'''获取电影信息 '''
    def __init__(self):
#        self.keywords='成人视讯'   #好像不好使，得继续研究
        self.log = mylog()
        self.pages = 20   #爬取的页数
        self.urls = []  #url池
        self.items = []
        self.getUrls(self.pages) #获取抓取页面的url
        self.browser = webdriver.Chrome()  #放这里是避免多次调用造成一直再打开新的chrome，用self属性为了可以传到函数里
        self.spider(self.urls)
        self.pipelines(self.items)
        
    
    def getResponseContent(self, url):
		#'''获取页面返回的数据 '''
        try:
#            response = browser.get(url)
            self.browser.get(url)
        except:
            self.log.error(u'Python 返回URL:%s  数据失败' %url)
        else:
            self.log.info(u'Python 返回URUL:%s  数据成功' %url)
            return self.browser
    
    def getUrls(self, pages):
        urlHead = 'http://cl.8qb.xyz/thread0806.php?fid=7&search=&page='
        for i in xrange(1,pages + 1):
            url = urlHead + str(i)
            self.urls.append(url)
            self.log.info(u'添加URL:%s 到URLS列表' %url)
    
    def spider(self, urls):
        for url in urls:
            htmlContent = self.getResponseContent(url)
            List = htmlContent.find_elements_by_xpath("//h3/a[contains(text(),'成人视讯')]")   #这是查找文本里的关键词表达
            for x in List:
                item = MovieItem()
                item.movieName=x.text
                item.movieNet=x.get_attribute('href')
                self.items.append(item)
                self.log.info(u'获取电影名为：<<%s>>成功' %(item.movieName))
    
    def pipelines(self, items):
        fileName = u'thefile.txt'
        with codecs.open(fileName, 'w', 'utf8') as fp:
            for item in items:
                fp.write('%s \t %s  \r\n' %(item.movieName, item.movieNet))
                self.log.info(u'电影名为：<<%s>>已成功存入文件"%s"...' %(item.movieName, fileName.decode('GBK')))
            

if __name__ == '__main__':
    GM = GetMovie()

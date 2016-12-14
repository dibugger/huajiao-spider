import scrapy
from scrapy.http.request import Request
from scrapy import Selector
from bs4 import BeautifulSoup
import re
from tutorial.items import UserItem


class Huajiao_Spider(scrapy.Spider):

    name = 'huajiao'

    def start_requests(self):
        allowed_domains = ['www.huajiao.com/']
        urls = ['1', '2', '3', '5', '999', '1000', '1001']
        for url in urls:
            newUrl = 'http://www.huajiao.com/category/' + url
            request = Request(url=newUrl, callback=self.filterPages, headers={
                              'Referral': 'http://www.huajiao.com/', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
            yield request

    def filterPages(self, response):
        bsObj = BeautifulSoup(response.text, 'html.parser')
        paginations = bsObj.find(name='ul', attrs={'class': 'pagination'})
        pages = paginations.find_all(name='a')
        for page in pages:
            if 'href' in page.attrs:
                newPage = page.attrs['href']
                request = Request(url=newPage, callback=self.filterLiveIds, headers={
                                  'Referral': 'http://www.huajiao.com/', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
                yield request

    def filterLiveIds(self, response):
        bsObj = BeautifulSoup(response.text, 'html.parser')

        # parse user
        for link in bsObj.find_all(name='a', href=re.compile("^(/l/)")):
            if 'href' in link.attrs:
                newPage = 'http://www.huajiao.com' + link.attrs['href']
                request = Request(url=newPage, callback=self.getUserId, headers={
                                  'Referral': 'http://www.huajiao.com/', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
                yield request

    def getUserId(self, response):
        bsObj = BeautifulSoup(response.text, 'html.parser')
        user = bsObj.find_all("a", href=re.compile("^(/user/[0-9]+)"))[0]
        if 'href' in user.attrs:
            newPage = 'http://www.huajiao.com' + user.attrs['href']
            request = Request(url=newPage, callback=self.parseUserStat, headers={
                              'Referral': 'http://www.huajiao.com/', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
            yield request

    def parseUserStat(self, response):
        bsObj = BeautifulSoup(response.text, 'html.parser')
        user_item = UserItem()
        try:
            user_info = bsObj.find(name='div', attrs={'id': 'userInfo'})
            user_item['avatar'] = user_info.find(
                name='div', attrs={'class': 'avatar'}).img.attrs['src']
            user_item['user_id'] = user_info.find(
                name='p', attrs={'class': 'user_id'}).get_text()
            activity_info = user_info.find(
                name='ul', attrs={'class': 'clearfix'})
            elems = activity_info.find_all('li')
            user_item['followings'] = elems[0].find(name='p').get_text()
            user_item['followers'] = elems[1].find(name='p').get_text()
            user_item['likes'] = elems[2].find(name='p').get_text()
            user_item['experience'] = elems[3].find(name='p').get_text()
            yield user_item
        except AttributeError:
            print(str("Error!") + ":html parse error in getUserData()")

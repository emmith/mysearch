# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from .items import DyttItem
class DyttSpider(CrawlSpider):
    name = 'dytt_spider'
    allowed_domains = ['ygdy8.net']
    start_urls = ['https://www.ygdy8.net/html/gndy/dyzz/']

    rules = (
        # 电影详情页链接
        Rule(LinkExtractor(restrict_xpaths='//a[@class="ulink"]'), callback='movie_detail'),
        # 下一页的链接
        Rule(LinkExtractor(allow=r'list_23_2.html'), follow=True),
        # Rule(LinkExtractor(allow=r'list_23_([0-9]+).html'), follow=True),
    )
    def movie_detail(self, response):
        '''在电影详情页提取电影信息'''
        item = DyttItem()
        item["title"] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract_first()

        # 下面是使用正则匹配（这个网站的网页太不规范了）
        response_str = response.text
        # 产地
        place = re.findall(r'◎产　　地　(.*?)<', response_str)
        item["country"] = place[0] if len(place) > 0 else None
        # 年代
        time = re.findall(r'◎年　　代　(.*?)<', response_str)
        item["date"] = time[0] if len(time) > 0 else None
        # 简介
        # 类型
        thetype = re.findall(r'◎类　　别　(.*?)<',response_str)
        item["type"] = thetype[0] if len(thetype) > 0 else None

        # 主演
        actor = re.findall(r'◎主　　演　([\w\W]*?)◎',response_str)

        item["starring"] = actor[0] if len(actor) > 0 else None
        # url
        item["url"] = response.url
        yield item


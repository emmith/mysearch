# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from dytt.items import DyttItem
import html.parser


class DyttSpider(CrawlSpider):
    name = 'dytt_spider'
    allowed_domains = ['ygdy8.net']
    start_urls = ['https://www.ygdy8.net/html/gndy/dyzz/']

    rules = (
        # 电影详情页链接
        Rule(LinkExtractor(restrict_xpaths='//a[@class="ulink"]'), callback='movie_detail'),
        # 下一页的链接
        Rule(LinkExtractor(allow=r'list_23_([0-9]+).html'), follow=True),
        # Rule(LinkExtractor(allow=r'list_23_([0-9]+).html'), follow=True),
    )

    def movie_detail(self, response):
        '''在电影详情页提取电影信息'''
        items = DyttItem()
        items["video_title"] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract_first()

        # 下面是使用正则匹配（这个网站的网页太不规范了）
        response_str = response.text
        # 产地
        items["country"] = find_info(r'◎产　　地　(.*?)<', response_str)
        # 年代
        items["release_date"] = find_info(r'◎上映日期　(.*?)\(', response_str)
        # 标签
        items["label"] = find_info(r'◎类　　别　(.*?)<', response_str)
        # 主演
        items["starring"] = find_info(r'◎主　　演　([\w\W]*?)◎', response_str, 1)
        # 导演
        items["director"] = find_info(r'◎导　　演　([\w\W]*?)◎', response_str, 1)
        # 详情
        items["description"] = find_info(r'◎简　　介([\w\W]*?)<a', response_str, 1)
        # url

        items["url"] = response.url

        # 直接返回最后数据
        return items


def handle(data):
    pattern = re.compile(r'<[^>]+>', re.S)
    temp = pattern.sub('', data)
    s = html.parser.unescape(temp)
    return "".join(s.split())


def find_info(pattern, response_str, num=0):
    info = re.findall(pattern, response_str)
    if len(info) > 0:
        info = info[0]
        if num == 1:
            info = handle(info)
        return info if len(info) > 0 else None
    return None

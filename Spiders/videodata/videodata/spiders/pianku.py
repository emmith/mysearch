# -*- coding: utf-8 -*-
import scrapy
from ..items import VideodataItem
import random,re
import json
import copy
ua_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50']

''' http://www.pianku.li/mv/------409.
html
'''

class PiankuSpider(scrapy.Spider):
    name = 'pianku'
    allowed_domains = ['www.pianku.li']
    start_urls = ['http://www.pianku.li/']
    custom_settings = {
        'ITEM_PIPELINES': {'videodata.pipelines.PiankuPipeline': 302,
                           'videodata.pipelines.ElasticsearchPipeline': 350
                           },

    }

    def parse(self, response):
        headers = {'user-agent': random.choice(ua_list)}
        item = VideodataItem()
        next_page = ['https://www.pianku.li/mv','https://www.pianku.li/tv','https://www.pianku.li/ac']

        for i in range(3):
            item_copy = copy.deepcopy(item)
            yield scrapy.Request(url=next_page[i],
                                 callback=self.parse_page,
                                 headers=headers,
                                 meta={'item': item_copy})

    def parse_page(self, response):
        item = response.meta['item']
        url = 'http://www.pianku.li'
        movies_info = response.css('[class="content-list"]>li')

        next_page_url_info = response.css('[class = "a1"]')
        # https://www.pianku.li/tv/------3.html
        next_page_url = url + next_page_url_info.re_first(r'href="(.*?)"')
        next_page_url.replace('\n', '').replace('\t', '').replace('\r', '').strip()
        print("next_page_url = " + next_page_url)
        next_page = next_page_url_info.re_first(r'.*------(\d+)')
        this_page = response.css('body > main > div.pages > span').re_first(r'(\d+)')
        if next_page != this_page:
            headers = {'user-agent': random.choice(ua_list)}
            for each_info in movies_info:
                headers = {'user-agent': random.choice(ua_list)}
                next_url = 'http://www.pianku.li' + each_info.re_first(r'<a href="(.*?)" title=".*?">')
                item['video_url'] = next_url
                if 'mv' in next_url:
                    item['sub_type'] = "电影"
                elif 'tv' in next_url:
                    item['sub_type'] = "电视剧"
                elif 'ac' in next_url:
                    item['sub_type'] = "动漫"
                #print("next_url = " + next_url)
                item_copy = copy.deepcopy(item)
                yield scrapy.Request(url=next_url,
                                     callback=self.parse_info,
                                     headers=headers,
                                     meta={'item': item_copy})
            item_copy = copy.deepcopy(item)
            yield scrapy.Request(url=next_page_url,
                                     callback=self.parse_page,
                                     headers=headers,
                                     meta={'item': item_copy})
        return item


    def parse_info(self, response):
        item = response.meta['item']
        movie_name = response.css('[class="main-ui-meta"]>h1').re_first(r'<h1>(.*?)<span class=".*?">.*?</span></h1>')
        item['video_title'] = movie_name
        video_year = response.css('[class="main-ui-meta"]>h1>span').re_first(r'(\d+)')
        item['release_date'] = video_year
        video_imgurl = response.css('[class="img cover"]>img').re_first(r'<img src="(.*?)" width=".*?" alt=".*?">')
        item['cover_url'] = video_imgurl
        video_info = response.css('[class="main-ui-meta"] > div ')
        #print(video_info)
        for each in video_info:
            list = each.re_first(r'<span>(.*?)</span>')
            #each_info = re.findall(r'<a href=".*?" target=".*?">(.*?)</a>',each)
            #print(each)
            if list is None:
                continue
            else :
                temp = list[:2]
            if temp == "导演":
                director = each.re_first(r'<a href=".*?">(.*?)</a>')
                item['director'] = director
            elif temp == "主演":
                actors_list = each.re(r'<a href=".*?" target=".*?">(.*?)</a>')
                actors = ",".join(actors_list)
                item['starring'] = actors
            elif temp == "类型":
                type_list = each.re(r'<a href=".*?" target=".*?">(.*?)</a>')
                type = ",".join(type_list)
                item['sub_type'] = type
            elif temp == "地区":
                area_list = each.re(r'<a href=".*?" target=".*?">(.*?)</a>')
                area = ",".join(area_list)
                item['location'] = area
        infos = response.css('[class="movie-introduce"] > p:nth-child(1)')
        infos_result = infos.re_first(r'<p>(.*?)</p>')
        if infos_result is None:
            infos_result = infos.re_first(r'<p class="zkjj_a">(.*?)</p>')

        item['description'] = infos_result
        numbers_info = response.css('[class="bottom2"]')
        numbers = numbers_info.re_first(r'<span class=".*?"><i class="icon-play"></i>.*?(\d+).*?</span>')
        if numbers is not None:
            item['episode'] = numbers
        else :
            item['episode'] = 1

        yield item

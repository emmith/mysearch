# -*- coding: utf-8 -*-
import scrapy
from ..items import VideodataItem
import random,re
import json
import copy
ua_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50']



class MjxSpider(scrapy.Spider):
    name = 'mjx'
    custom_settings = {
        'ITEM_PIPELINES': {'videodata.pipelines.MjxPipeline': 301,
                           'videodata.pipelines.ElasticsearchPipelineMjx': 355},
    }
    allowed_domains = ['www.meijuxia.net']
    start_urls = ['http://www.meijuxia.net/video/type/2------hits.html']

    def parse(self, response):
        headers = {'user-agent': random.choice(ua_list)}
        item = VideodataItem()
        #总页数 331
        all_page = 331
        next_url = ""
        for i in range(2,all_page+1):
            if i==1:
                next_url = 'http://www.meijuxia.net/video/type/2------hits.html'
            elif i>1:
                next_url = 'http://www.meijuxia.net/video/type/2------hits-' + str(i) + '.html'
            #print(next_url)
            # 以下全部使用深拷贝避免变量共享问题
            item_copy = copy.deepcopy(item)
            list1 = []
            list1.append(next_url)
            #item['page_url'] = next_url
            print("next_url = " + next_url)
            #print(item['page_url'])
            yield scrapy.Request(url=next_url,
                                callback=self.parse_each_page,
                                headers=headers,
                                meta={'item': item_copy})

    def parse_each_page(self, response):
        item = response.meta['item']
        first_list = response.css('[class="padding col-xs-4 col-sm-3 col-md-2"]')
        for each in first_list:
            headers = {'user-agent': random.choice(ua_list)}
            each_url = each.re_first(r'href="(.*?)"')
            real_url = 'http://www.meijuxia.net' + each_url
            # print(real_url)
            item['video_url'] = real_url
            real_name = each.re_first(r'title="(.*?)"')
            #print(real_name)
            item['video_title'] = real_name
            # 以下全部使用深拷贝避免变量共享问题
            item_copy = copy.deepcopy(item)
            yield scrapy.Request(item['video_url'],
                             callback=self.parse_each_info,
                             headers=headers,
                             meta={'item': item_copy})

    def parse_each_info(self, response):
        item = response.meta['item']
        imgurl = response.css('[class="video-item"]')
        imgurl2 = imgurl.re_first(r'data-original="(.*?)"')
        real_imgurl = ""
        if imgurl2[0] == '/':
            #http://www.meijuxia.net/index.php?g=home&m=images&a=read&url=aHR0cHM6Ly9pbWc5LmRvdWJhbmlvLmNvbS92aWV3L3Bob3RvL3NfcmF0aW9fcG9zdGVyL3B1YmxpYy9wMjQ1OTYxNDQ4Ny5qcGc=
            real_imgurl = 'http://www.meijuxia.net' + imgurl2
        elif imgurl2[0] == 'h':
            real_imgurl = imgurl2

        item['cover_url'] = real_imgurl
        director_info = response.css('[class="detail-actor clearfix"]>li:nth-child(1)>a[href$="l"]')
        director_list = []
        for each in director_info:
            #print(type(each))
            #each_director =  re.match(r'<a href=".*?">(.+?)</a>', each)
            each_director = each.re_first(r'<a href=".*?">(.+?)</a>')
            director_list.append(each_director)
        #print(item['name'] + " : " )
        #print(",".join(director_list))
        if director_list != None:
            if None in director_list:
                director_list.remove(None)
            director_list_str = ",".join(director_list)
            item['director'] = director_list_str

        actors_info = response.css('[class="detail-actor clearfix"]>li:nth-child(2)>a[href$="l"]')
        actors_list = []
        for each in actors_info:
            each_actors = each.re_first(r'<a href=".*?">(.+?)</a>')
            actors_list.append(each_actors)
        if actors_list != None:
            if None in actors_list:
                actors_list.remove(None)
            actors_list_str = ",".join(actors_list)
            item['starring'] = actors_list_str

        type_info = response.css('[class="detail-actor clearfix"]>li:nth-child(3)> span:nth-child(1) > a[href]')
        type_list = []
        for each in type_info:
            each_type = each.re_first(r'<a href=".*?">(.+?)</a>')
            type_list.append(each_type)
        # type_list = ['string', None]


        if type_list != None:
            if None in type_list:
                type_list.remove(None)
            type_list_str = ",".join(type_list)
            item['sub_type'] = type_list_str

        item['video_type'] = "电视剧"

        area_info = response.css('[class="detail-actor clearfix"]>li:nth-child(3)> span:nth-child(2) > a[href]')
        area_list = []
        for each in area_info:
            each_area = each.re_first(r'<a href=".*?">(.+?)</a>')
            area_list.append(each_area)
        if  area_list != None:
            if None in area_list:
                area_list.remove(None)
            area_list_str = ",".join(area_list)
            item['location'] = area_list_str

        year_info = response.css('[class="detail-actor clearfix"]>li:nth-child(3)> span:nth-child(3) > a[href]')
        final_year_info = year_info.re_first(r'<a href=".*?">(.+?)</a>')
        item['release_date'] = final_year_info

        main_info = response.css('[class="vod_content padding"]')
        final_main_info = main_info.re_first(r'<div class="vod_content padding">(\s*.+?)</div>')
        item['description'] = final_main_info

        # [class="list-unstyled row text-center tab-pane ff-playurl ff-playurl-tab-1 active fade in"]>li

        number_info = response.css('[class ="tab-content ff-playurl-tab"]>ul:nth-child(1)>li')
        number_count = 0
        for each in number_info:
            number_count += 1
        item['episode'] = number_count
        yield item
        #http://www.meijuxia.net/index.php?g=home&m=images&a=read&url=aHR0cHM6Ly9pbWc5LmRvdWJhbmlvLmNvbS92aWV3L3Bob3RvL3NfcmF0aW9fcG9zdGVyL3B1YmxpYy9wMjQ1OTYxNDQ4Ny5qcGc=
        #http://www.meijuxia.net/index.php?g=home&amp;m=images&amp;a=read&amp;url=aHR0cHM6Ly9pbWc5LmRvdWJhbmlvLmNvbS92aWV3L3Bob3RvL3NfcmF0aW9fcG9zdGVyL3B1YmxpYy9wMjA1NjA0NDM0NC5qcGc=
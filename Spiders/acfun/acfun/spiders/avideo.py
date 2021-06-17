import scrapy
import logging
from scrapy import Request
from ..items import AcfunItem
import random, re
import copy

ua_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50']


def num_helper(str):
    if str.endswith('万'):
        s = int(float(str[:-1])*10000)
    else:
        s = int(str)
    return s


class AvideoSpider(scrapy.Spider):
    name = 'avideo'
    allowed_domains = ['www.acfun.cn']
    start_urls = ['https://www.acfun.cn/v/list86/index.htm']

    def parse(self, response):
        # 一级大标题获取

        all_first_title_ele = response.css('[class="first-item"]')
        del (all_first_title_ele[0])

        # 包含二级标题
        all_second_title_ele = response.css('[class="second-container"]>ul')
        for first_title, second_title in zip(all_first_title_ele, all_second_title_ele):
            if first_title in ['AC正义', '番剧', '文章', '直播']:
                continue
            item = AcfunItem()
            # 利用正则表达式提取一级标题
            title = first_title.re_first(r'<a.*?>(.*?)</a>')
            item['video_type'] = title
            for st in second_title.css('a'):
                headers = {'user-agent': random.choice(ua_list)}
                # 获取二级标题
                item['sub_type'] = st.re_first(r'<a.*?>(.*?)</a>')
                item['type_url'] = 'https://www.acfun.cn' + st.re_first(r'href="(.*?)"')
                # 以下全部使用深拷贝避免变量共享问题
                item_copy = copy.deepcopy(item)

                # yield item
                yield scrapy.Request(item['type_url'],
                                     callback=self.parse_video_title,
                                     headers=headers,
                                     meta={'item': item_copy})

        # 解析真正的请求地址（观察network）

    def parse_video_title(self, response):
        item = response.meta['item']

        # 切换页数
        for page in range(5):
            headers = {'user-agent': random.choice(ua_list)}

            url = item['type_url'] + '?sortField=viewCount&duration=all&date=default&page=' + str(page)
            yield scrapy.Request(url, callback=self.parse_another_videos, headers=headers,
                                 meta={'item': copy.deepcopy(item)})
            # yield item

        # 从真正请求的url获取标题、视频封面、视频描述、up主、视频url、观看数、评论数

    def parse_another_videos(self, response):

        item = response.meta['item']

        # 所有视频标题（未处理）
        all_half_video_title = response.css('[class="list-content-title"]')
        # 所有视频封面（未处理）
        all_half_video_cover = response.css('[class="list-content-top"]')
        # 所有up主（未处理）
        all_half_video_up = response.css('[class="list-content-item"]')

        for half_title, half_cover, half_up in zip(all_half_video_title, all_half_video_cover, all_half_video_up):
            headers = {'user-agent': random.choice(ua_list)}

            item['video_title'] = half_title.re_first(r'<a.*?>(.*?)</a>')
            item['director'] = half_up.re_first(r'<a.*?>UP:(.*?)</a>')
            item['cover_url'] = half_cover.re_first(r'src="(.*?)"')
            item['video_url'] = "https://www.acfun.cn" + half_title.re_first(r'href="(.*?)"')
            item['view'] = num_helper(half_cover.re_first(r'<span class="viewCount">(.*?)</span>'))
            # item['view'] = half_cover.re_first(r'<span class="viewCount">(.*?)</span>')
            item['comment'] = num_helper(half_cover.re_first(r'<span class="commentCount">(.*?)</span>'))
            # item['comment'] = half_cover.re_first(r'<span class="commentCount">(.*?)</span>')

            yield scrapy.Request(item['video_url'], callback=self.parse_video_description, headers=headers,
                                 meta={'item': copy.deepcopy(item)})

    def parse_video_description(self, response):
        item = response.meta['item']

        item['description'] = response.css('[class="description-container"]')[0].re_first(r'<div.*?>(.*?)</div>')
        yield item

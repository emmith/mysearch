import scrapy
from bili.items import BiliItem
import re

class BiliRankingSpider(scrapy.Spider):
    name = 'video_bili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['https://www.bilibili.com/v/popular/rank/all']
    url_list_en = ['bangumi', 'guochan', 'guochuang', 'documentary', 'douga', 'music', 'dance',
                   'game', 'technology', 'digital', 'car', 'life', 'food', 'animal', 'kichiku',
                   'fashion', 'ent', 'cinephile', 'movie', 'tv', 'origin', 'rookie']
    url_list_zh = ['全站', '番剧', '国产动画', '国创相关', '纪录片', '动画', '音乐', '舞蹈', '游戏', '知识', '数码',
                   '汽车', '生活', '美食', '动物圈', '鬼畜', '时尚', '娱乐', '影视', '电影', '电视剧', '原创', '新人']
    urls = ['https://www.bilibili.com/v/popular/rank/' + i for i in url_list_en]
    dictionary = dict(zip(url_list_en, url_list_zh[1:]))
    dictionary['all'] = '全站'

    def parse(self, response):

        video_type = response.xpath('//div[@class="info"]/a/text()').extract()  # 视频名称
        rank = response.xpath('//div[@class="num"]/text()').extract()  # 视频排名
        director = response.xpath('//div[@class="info"]/div[@class="detail"]/a/span/text()').extract()  # 视频作者
        total_score = response.xpath('//div[@class="info"]/div[@class="pts"]/div/text()').extract()  # 视频得分
        play_volume = response.xpath('//div[@class="info"]/div[@class="detail"]/span[1]/text()').extract()  # 视频播放量
        url = response.xpath('//div[@class="info"]/a[@class="title"]/@href').extract()
        label = BiliRankingSpider.dictionary[re.split('/', response.url)[-1]]
        for n, r, a, s, p, l in zip(video_type, rank, director, total_score, play_volume, url):
            items = BiliItem()

            items['rank'] = str(r).strip()
            items['video_title'] = str(n).strip()
            items['director'] = str(a).strip()
            items['total_score'] = str(s).strip()
            items['play_volume'] = str(p).strip()
            items['url'] = str(l).strip()
            items['label'] = label
            yield items

        if len(self.urls) > 0:
            url = self.urls.pop(0)
            # 这里回调parse这个函数，接着爬取动画和国创相关排行榜
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            return

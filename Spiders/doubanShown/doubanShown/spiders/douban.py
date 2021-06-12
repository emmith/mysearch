import scrapy
from scrapy.http import Request
from ..items import DoubanItem
from scrapy.selector import Selector

class DoubanSpider(scrapy.Spider):
    name = 'video_doubanShown'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://www.douban.com/doulist/3524358/']
    # 主站链接 用来拼接
    url = 'https://www.douban.com/doulist/3524358/'

    def parse(self, response):
        item = DoubanItem()  # 实例化Item类，用于保存读取的数据
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="bd doulist-subject"]')  # 选择电影信息区域
        for eachMovie in Movies:
            halfVideoUrl=eachMovie.xpath('div[1]/a[1]/@href').extract()
            if(len(halfVideoUrl)>0):
                item['video_url']=halfVideoUrl[0]

            videoTitle=eachMovie.xpath('div[@class="title"]/a/text()').extract() #有的title是第一个，有的是第二个，网站不规范
            if len(videoTitle)==1:
                item['video_title']=videoTitle[0].strip()
            else:
                item['video_title']=videoTitle[1].strip()

            score=eachMovie.xpath('div[@class="rating"]/span[2]/text()').re(r'[0-9].[0-9]') #可能有的没评分
            if len(score)==1:
                item['score']=score[0]
            else:
                item['score']=0.0

            comment=eachMovie.xpath('div[@class="rating"]/span[3]/text()')
            if len(comment)>0:
                item['comment']=comment.re(r'([0-9])')[0]

            abstract=eachMovie.xpath('div[@class="abstract"]/text()')
            info=['director','starring','video_type','location','release_date']
            for index,i in enumerate(abstract):
                item[info[index]]=i.re(r'(?<=:).*')[0].strip() #提取出冒号后面的字符
            yield item
        nextLink = selector.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()  # 构造下一页的链接
        if nextLink:  # 判断是否到了最后一页
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(nextLink, callback=self.parse)  # 循环访问链接
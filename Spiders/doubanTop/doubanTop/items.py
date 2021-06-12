# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DoubanItem(scrapy.Item):
    video_type = scrapy.Field()
    video_title = scrapy.Field()
    director=scrapy.Field()
    starring=scrapy.Field()
    score=scrapy.Field()
    comment=scrapy.Field()
    video_url=scrapy.Field()
    location=scrapy.Field()
    release_date=scrapy.Field()

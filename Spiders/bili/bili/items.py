# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiliItem(scrapy.Item):
    # define the fields for your item here like:
    video_title = scrapy.Field()
    rank = scrapy.Field()
    total_score = scrapy.Field()
    director = scrapy.Field()
    play_volume = scrapy.Field()
    url = scrapy.Field()
    label = scrapy.Field()
    pass

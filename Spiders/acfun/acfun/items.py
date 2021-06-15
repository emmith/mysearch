# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AcfunItem(scrapy.Item):
    # define the fields for your item here like:
    video_type = scrapy.Field()
    sub_type = scrapy.Field()
    type_url = scrapy.Field()
    video_title = scrapy.Field()
    description = scrapy.Field()
    director = scrapy.Field()
    cover_url = scrapy.Field()
    video_url = scrapy.Field()
    view = scrapy.Field()
    comment = scrapy.Field()



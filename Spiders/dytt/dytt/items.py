# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
class DyttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_title = scrapy.Field()
    release_date = scrapy.Field()
    country = scrapy.Field()
    url = scrapy.Field()
    director = scrapy.Field()
    starring = scrapy.Field()
    label = scrapy.Field()
    description = scrapy.Field()
    pass
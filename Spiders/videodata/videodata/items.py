# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VideodataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名称
    ## name -> video_title
    video_title = scrapy.Field()
    # 剧集地址
    ## url -> video_url
    video_url = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 主演
    ## actors->starring
    starring = scrapy.Field()
    # 类型
    # type->video_type
    video_type = scrapy.Field()
    # 子类型
    sub_type = scrapy.Field()
    # 地区
    ## area -> location
    location = scrapy.Field()
    # 上映年份
    # year->release_date
    release_date = scrapy.Field()
    # 剧集简介
    ## info->description
    description = scrapy.Field()
    # 剧集数量
    #numbers ->episode
    episode = scrapy.Field()
    # 剧集封面
    ## img_url->cover_url
    cover_url = scrapy.Field()


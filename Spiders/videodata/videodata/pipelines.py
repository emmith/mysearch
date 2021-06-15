# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
import datetime

#from .videodata.models.es_types import videodataType
from .models.es_mjx import videodataTypeMjx
from .models.es_types import videodataType


class VideodataPipeline:
    def process_item(self, item, spider):
        if item['info'] != None:
            item['info'] = self.process_info(item['info'])
        if item['img_url'] != None:
            item['img_url'] = self.process_img_url(item['img_url'])
        #print(item)
        return item

    def process_info(self, info):
        return info.replace('\n', '').replace('\t', '').replace('\r', '').strip()

    def process_img_url(self, info):
        return info.replace('\n', '').replace('\t', '').replace('\r', '').replace('amp;', '').strip()

class MjxPipeline(object):
    def process_item(self, item, spider):
        if item['description'] != None:
            item['description'] = self.process_info(item['description'])
        if item['cover_url'] != None:
            item['cover_url'] = self.process_img_url(item['cover_url'])
        #self.writer.writerow(item)

        #print(item)
        return item

    def process_info(self, info):
        return info.replace('\n', '').replace('\t', '').replace('\r', '').strip()

    def process_img_url(self, info):
        return info.replace('\n', '').replace('\t', '').replace('\r', '').replace('amp;', '').strip()

    #def __init__(self):
     #   d = datetime.datetime.now().strftime(r'%Y-%m-%d&%H-%M&')
        # csv文件的位置,无需事先创建
     #   store_file = d + 'mjx.csv'
        # 打开(创建)文件
     #   self.file = open(store_file, "a", newline="", encoding='utf-8-sig')
        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
     #   self.fieldnames = ["actors", "area", "director", "img_url", "info", "name", "numbers", "type", "url", "year"]
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
      #  self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
      #  self.writer.writeheader()


    #def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
     #   self.file.close()


class PiankuPipeline(object):
    def process_item(self, item, spider):
        if item['description'] != None:
            item['description'] = self.process_info(item['description'])
        if item['cover_url'] != None:
            item['cover_url'] = self.process_img_url(item['cover_url'])
        #self.writer.writerow(item)
        #print(item)
        return item

    def process_info(self, info):
        return info.replace('\n', '').replace('\t', '').replace('\r', '').replace('\u3000','').replace('<br>','').replace('<span '
         'class="zk_jj">[展开全部]</span>','').strip()

    def process_img_url(self, info):
        return info.replace('\n', '').replace('\t', '').replace('\r', '').replace('amp;', '').strip()

    #def __init__(self):
    #    d = datetime.datetime.now().strftime(r'%Y-%m-%d&%H-%M&')
        # csv文件的位置,无需事先创建
    #    store_file = d + 'pianku.csv'
        # 打开(创建)文件
    #    self.file = open(store_file, "a", newline="", encoding='utf-8-sig')
        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
    #    self.fieldnames = ["actors", "area", "director", "img_url", "info", "name", "numbers", "type", "url", "year"]
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
    #    self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
    #    self.writer.writeheader()


    #def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
    #    self.file.close()

class ElasticsearchPipeline:

    def process_item(self, item, spider):
        vd = videodataType(item)
        vd.save()
        return item

class ElasticsearchPipelineMjx:

    def process_item(self, item, spider):
        vd = videodataTypeMjx(item)
        vd.save()
        return item


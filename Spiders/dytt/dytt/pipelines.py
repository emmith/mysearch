# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from dytt.models.es_type import DyttType
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DyttPipeline:
    def process_item(self, item, spider):
        return item


class DyttMysqlPipeline:
    def __init__(self):
        self.connect = mysql.connector.connect(
            user="root",
            password="123456",
            port=3306,
            database='test',
            auth_plugin='mysql_native_password')
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 数据入库
        sql = "insert into `dytt` (`title`,`download_url`) values ('%s','%s')" % \
              (item['title'], item['url'])
        self.cursor.execute(sql)
        self.connect.commit()
        # 这里的return不能省略
        return item

    def close_spider(self, spiders):
        self.connect.close()


class ElasticsearchPipeline:

    def process_item(self, item, spider):
        sn = DyttType(item)
        sn.save()
        return item

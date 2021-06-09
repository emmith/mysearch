import mysql.connector
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BiliPipeline:
    def process_item(self, item, spider):
        return item

class BiliMysqlPipeline:
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
        sql = "insert into `bili_rank` (`rank`,`name`,`score`,`author`,`playvolume`,`link`) values ('%s','%s','%s','%s','%s','%s')" % \
              (item['rank'],item['name'],item['score'],item['author'],item['play_volume'],item['link'])
        self.cursor.execute(sql)
        self.connect.commit()
        # 这里的return不能省略
        return item


from .models.es_type import BiliType

class ElasticsearchPipeline:

    def process_item(self, item, spider):
        sn = BiliType(item)
        sn.save()
        return item
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .models.es_types import Video


class AcfunPipeline:
    # def process_item(self, item, spider):
    #     return item
    def process_item(self, item, spider):
        item['video_title'] = self.process_title(item['video_title'])
        print(item)
        return item

    def process_title(self, title):
        return title.replace('\n', '').replace('\t', '').strip()


class ElasticsearchPipeline:

    def process_item(self, item, spider):
        ac = Video(item)
        ac.save()
        return item

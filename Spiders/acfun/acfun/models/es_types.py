# -*- codeing: utf-8 -*-
from elasticsearch_dsl import Document, Keyword, Text, Long
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['127.0.0.1'])


class Video(Document):
    # 设置index名称和document名称
    class Index:
        name = "video_acfun"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
        mappings = {
            "properties": {
                "video_type": {
                    "type": "keyword"
                },
                "sub_type": {
                    "type": "keyword"
                },
                "video_title": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "director": {
                    "type": "keyword"
                },
                "cover_url": {
                    "type": "keyword"
                },
                "video_url": {
                    "type": "keyword"
                },
                "view": {
                    "type": "long"
                },
                "comment": {
                    "type": "long"
                }
            }
        }

    # TODO:fileds定义
    video_type = Keyword()  # 不分词，默认保留256个字符
    sub_type = Keyword()
    video_title = Text(
        analyzer="ik_max_word"
    )
    description = Text(
        analyzer="ik_max_word"
    )
    director = Keyword()
    cover_url = Keyword()
    video_url = Keyword()
    view = Long()
    comment = Long()

    def __init__(self, item):
        super(Video, self).__init__()  # 调一下父类的init，避免init重写导致一些init操作没执行
        self.assignment(item)

    # TODO:将item转换为es的数据
    def assignment(self, item):
        # TODO：给没爬到的字段赋默认值：空串
        keys = ['video_type',
                'sub_type',
                'video_title',
                'description',
                'director',
                'cover_url',
                'video_url',
                'view',
                'comment']
        for key in keys:
            try:
                item[key]
            except:
                item[key] = ''
        # TODO：将字段值转换为es的数据
        # 虽然只是将原来的item值赋给了成员变量，但这个过程中会执行数据格式转换操作，
        # 比如url本来在item是python的字符串类型，转换后变为es的keyword类型
        self.video_type = item['video_type']
        self.sub_type = item['sub_type']
        self.video_title = item['video_title']
        self.description = item['description']
        self.director = item['director']
        self.cover_url = item['cover_url']
        self.video_url = item['video_url']
        self.view = item['view']
        self.comment = item['comment']

        # # 或者简化代码为
        # for key in keys:
        #     vars(self)[key] = item[key]


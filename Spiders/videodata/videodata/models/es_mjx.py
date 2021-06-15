# -*- codeing: utf-8 -*-
# InnerDoc
from elasticsearch_dsl import Document, Keyword, Text, Date ,Integer, Completion
from elasticsearch_dsl.connections import connections

es = connections.create_connection(hosts=['localhost'])

class videodataTypeMjx(Document):
    # 设置index名称和document名称
    class Index:
        name = "video_meijiuxia"
        doc_type = "_doc"
        settings = {
          "number_of_shards": 1,
          "number_of_replicas": 0,
        }
        mappings = {
            "properties": {
                "video_title": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "release_date": {
                    "type": "date"
                },
                "episode": {
                    "type": "integer"
                },
                "sub_type": {
                    "type": "keyword"
                },
                "video_type": {
                    "type": "keyword"
                },
                "video_url": {
                    "type": "keyword"
                },
                "director": {
                    "type": "keyword"
                },
                "starring": {
                    "type": "keyword"
                },
                "location": {
                    "type": "keyword"
                },
                "cover_url": {
                    "type": "keyword"
                }
            }
        }

    # TODO:fileds定义
    video_title = Text(analyzer="ik_max_word")
    video_url = Keyword()
    director = Keyword()
    starring = Keyword()
    video_type = Keyword()
    sub_type = Keyword()
    location = Keyword()
    release_date = Date()
    description = Text(analyzer="ik_smart")
    episode = Integer()
    cover_url = Keyword()

    # TODO: 搜索建议，这么写为了防止报错
    from elasticsearch_dsl.analysis import CustomAnalyzer
    ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])
    suggest = Completion(analyzer=ik_analyzer)

    def __init__(self,item):
        super(videodataTypeMjx, self).__init__()#调一下父类的init，避免init重写导致一些init操作没执行
        self.assignment(item)

    # TODO:将item转换为es的数据
    def assignment(self, item):
        # TODO：给没爬到的字段赋默认值：空串
        keys = ['video_title',
                'video_url',
                'director',
                'starring',
                'video_type',
                'sub_type',
                'location',
                'release_date',
                'description',
                'episode',
                'cover_url']
        for key in keys:
            try:
                item[key]
            except:
                item[key] = ''
        # TODO：将字段值转换为es的数据
        self.video_title = item['video_title']
        self.video_url = item['video_url']
        self.director = item['director']
        self.starring = item['starring']
        self.video_type = item['video_type']
        self.sub_type = item['sub_type']
        self.location = item['location']
        self.release_date = item['release_date']
        self.description = item['description']
        self.episode = item['episode']
        self.cover_url = item['cover_url']

        self.suggest = self.gen_suggests(((self.video_title, 10), (self.video_type, 3), (self.director, 1)))

    def gen_suggests(self, info_tuple):
        # 根据字符串生成搜索建议数组
        used_words = set()  # set为去重功能
        suggests = []
        for text, weight in info_tuple:
            if text:
                # 字符串不为空时，调用elasticsearch的analyze接口分析字符串（分词、大小写转换）
                words = es.indices.analyze(body={'text': text, 'analyzer': "ik_max_word"})
                print(words)
                anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
                # analyzed_words = []
                # for r in words["tokens"]:
                #     if len(r["tokens"]) > 1:
                #         analyzed_words.append(r["tokens"])
                # anylyzed_words = set(analyzed_words)

                new_words = anylyzed_words - used_words
            else:
                new_words = set()

            if new_words:
                suggests.append({'input': list(new_words), 'weight': weight})
        return suggests

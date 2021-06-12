# -*- codeing: utf-8 -*-
from elasticsearch_dsl import Document, Keyword, Text, Double, Long, Date, Completion
from elasticsearch_dsl.connections import connections

es=connections.create_connection(host="127.0.0.1")

class doubanType(Document):
    # 设置index名称和document名称
    class Index:
        name = "video_doubantop"
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
                "comment":{
                    "type":"long"
                },
                "video_type":{
                    "type":"keyword"
                },
                "director":{
                    "type":"keyword"
                },
                "starring":{
                    "type":"keyword"
                },
                "score":{
                    "type":"double"
                },
                "video_url":{
                    "type":"keyword"
                },
                "location":{
                    "type":"keyword"
                },
                "release_date":{
                    "type":"date"
                }
            }
        }

    # TODO:fileds定义
    video_type = Keyword()
    video_title = Text(analyzer="ik_max_word")
    director = Keyword()
    starring = Keyword()
    score = Double()
    comment = Long()
    video_url = Keyword()
    location = Keyword()
    release_date = Date()

    # TODO: 搜索建议，这么写为了防止报错
    from elasticsearch_dsl.analysis import CustomAnalyzer
    ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])
    suggest = Completion(analyzer=ik_analyzer)

    def __init__(self,item):
        super(doubanType, self).__init__()#调一下父类的init，避免init重写导致一些init操作没执行
        self.assignment(item)

    # TODO:将item转换为es的数据
    def assignment(self, item):
        # TODO：给没爬到的字段赋默认值：空串
        keys = ['video_type',
                'video_title',
                'director',
                'starring',
                'score',
                'comment',
                'video_url',
                'location',
                'release_date']

        for key in keys:
            try:
                item[key]
            except:
                item[key] = ''
        # TODO：将字段值转换为es的数据
        # 虽然只是将原来的item值赋给了成员变量，但这个过程中会执行数据格式转换操作，
        # 比如url本来在item是python的字符串类型，转换后变为es的keyword类型
        self.video_type = item['video_type']
        self.video_title = item['video_title']
        self.director = item['director']
        self.starring = item['starring']
        self.score = item['score']
        self.comment = item['comment']
        self.video_url = item['video_url']
        self.location = item['location']
        self.release_date = item['release_date']

        # # 或者简化代码为
        # for key in keys:
        #     vars(self)[key]=item[key]
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
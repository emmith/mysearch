from django.db import models

# Create your models here.
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Keyword, Text, Double, Integer, Completion

connections.create_connection(hosts=['localhost'])


class BiliType(Document):
    class Index:
        name = "video_bili"
        doc_type = "_doc"

    video_title = Text(analyzer = "ik_max_word")
    rank = Integer()
    video_score = Integer()
    director = Keyword()
    play_volume = Text()
    video_url = Keyword()
    video_type = Keyword()

    suggest = Completion()


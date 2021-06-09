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
    total_score = Integer()
    director = Keyword()
    play_volume = Text()
    url = Keyword()
    label = Keyword()

    suggest = Completion()


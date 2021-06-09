from django.test import TestCase

# Create your tests here.
# 相关导入
import time
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es = Elasticsearch("localhost")
# using参数是指定Elasticsearch实例对象，index指定索引，可以缩小范围，index接受一个列表作为多个索引，且也可以用正则表示符合某种规则的索引都可以被索引，如index=["bank", "banner", "country"]又如index=["b*"]后者可以同时索引所有以b开头的索引，search中同样可以指定具体doc-type
s = Search(using=es, index="video_bili")

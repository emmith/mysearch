from django.shortcuts import render

# Create your views here.

import json
from django.views.generic.base import View
from search.models import BiliType
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from datetime import datetime
import redis

client = Elasticsearch(hosts=["127.0.0.1"])
redis_cli = redis.StrictRedis()

response = client.search(
    index="video_bili",
    body={
    }
)
redis_cli.set("count_bili", response['hits']['total']['value'])
response = client.search(
    index="video_dytt",
    body={
    }
)
redis_cli.set("count_dytt", response['hits']['total']['value'])

response = client.search(
    index="video_doubanTop",
    body={
    }
)
redis_cli.set("count_doubanTop", response['hits']['total']['value'])
response = client.search(
    index="video_doubanShown",
    body={
    }
)
redis_cli.set("count_doubanShown", response['hits']['total']['value'])


class IndexView(View):
    # 首页
    def get(self, request):
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        topn_search = [item.decode('utf8') for item in topn_search]
        # topn_search = []
        return render(request, "index.html", {"topn_search": topn_search})


# Create your views here.
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')  # 获取url中参数s的值
        re_datas = []

        if key_words:
            # suggest官网https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html
            # TODO:completion的方法 （非dsl）
            # response = client.search(
            #     index="video_bili",
            #     body={
            #         "suggest": {
            #             "my_suggest": {
            #                 "prefix": key_words,
            #                 "completion": {
            #                     "field": "suggest",
            #                     "fuzzy": {
            #                         "fuzziness": 10
            #                     },
            #                     "size": 10
            #                 }
            #             }
            #         }
            #     }
            # )
            # suggestions = response["suggest"]["my_suggest"][0]['options']
            # for match in suggestions:
            #     source = match['_source']
            #     re_datas.append(source["video_title"])

            # TODO:completion的方法 （dsl）
            # s = suningType.search()
            # s = s.suggest('my_suggest', key_words, completion = {
            #     "field": "suggest", "fuzzy": {
            #         "fuzziness": 2
            #     },
            #     "size": 10
            # })
            # suggestions = s.execute_suggest()
            # for match in suggestions.my_suggest[0].options:
            #     source = match._source
            #     re_datas.append(source["video_title"])

            # TODO:match的方法
            response = client.search(
                index=['video_dytt', 'video_bili', 'video_doubanTop', 'video_doubanShown'],
                body={
                    "_source": "video_title",
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["video_title", "video_type"]
                        }
                    },
                    "size": 5
                }
            )
            for hit in response["hits"]["hits"]:
                re_datas.append(hit["_source"]["video_title"])

        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    def get(self, request):
        # 获取搜索关键字
        key_words = request.GET.get("q", "")
        # 获取当前选择搜索的范围
        source = request.GET.get("s", "")

        redis_cli.zincrby("search_keywords_set", 1, key_words)  # 该key_words的搜索记录+1

        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        topn_search = [item.decode('utf8') for item in topn_search]
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1

        # 从redis查看该类数据总量，这边是从上面获取最开始query放入redis的数据总量
        count_bili = redis_cli.get("count_bili").decode('utf8')
        count_dytt = redis_cli.get("count_dytt").decode('utf8')
        count_doubanTop = redis_cli.get("count_doubanTop").decode('utf8')
        count_doubanShown = redis_cli.get("count_doubanShown").decode('utf8')

        start_time = datetime.now()
        # 根据关键字查找
        response = client.search(
            # 默认从电影天堂上搜索
            index=[source],
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["video_title", "director", "starring"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                # 对关键字进行高光标红处理
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "video_title": {},
                        "director": {},
                        "starring": {}
                    }
                }
            }
        )

        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]['value']
        # 分页
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)

        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "video_title" in hit["highlight"]:
                hit_dict["video_title"] = "".join(hit["highlight"]["video_title"])
            else:
                hit_dict["video_title"] = hit["_source"]["video_title"]

            hit_dict["video_title"] = handle_null_data("video_title", hit["_source"])
            hit_dict["director"] = handle_null_data("director", hit["_source"])
            hit_dict["video_url"] = handle_null_data("video_url", hit["_source"])
            hit_dict["video_type"] = handle_null_data("video_type", hit["_source"])
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)

        # 通过render返回给前端
        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,
                                               "count_dytt": count_dytt,
                                               "count_bili": count_bili,
                                               "count_doubanTop": count_doubanTop,
                                               "count_doubanShown": count_doubanShown,
                                               "topn_search": topn_search})


def handle_null_data(str, hits):
    if str in hits.keys():
        return hits[str]
    else:
        return "未爬取到"

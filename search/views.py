from django.shortcuts import render

# Create your views here.

import json
from django.views.generic.base import View
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from datetime import datetime
import redis

client = Elasticsearch(hosts=["127.0.0.1"])
redis_cli = redis.StrictRedis()

# 把video_后缀后面的部分放入下面的list
# 例如video_bili 则放入 bili
index_list = ["bili", "dytt", "doubantop", "doubanshown", "meijuxia", "pianku", "acfun"]
for i in index_list:
    response = client.search(
        index="video_" + i,
        body={
        }
    )
    redis_cli.set("count_" + i, response['hits']['total']['value'])


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

            # TODO:match的方法
            response = client.search(
                index=["video_" + i for i in index_list],
                body={
                    "_source": ["video_title"],
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["video_title", "video_type", "starring"]
                        }
                    },
                    "size": 10
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
        searchRange = request.GET.get("s", "")
        # 默认在这几个库中找
        source = ["video_dytt", "video_bili", "video_doubanshown", "video_doubantop", "video_meijuxia",
                  "video_pianku", "video_acfun"]
        if len(searchRange) != 0:  # 如果参数没有提交，返回一个空的字符串
            source = [searchRange]
        # 获取当前选择的搜索依据（按照title还是按照导演）
        searchType = request.GET.get("s_type", "")
        # 默认在这几个字段中查找
        fields = ["video_title", "director", "starring", "video_type"]
        if len(searchType) != 0:
            fields = [searchType]

        redis_cli.zincrby("search_keywords_set", 1, key_words)  # 该key_words的搜索记录+1

        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        topn_search = [item.decode('utf8') for item in topn_search]
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1

        # 从redis查看该类数据总量，这边是从上面获取最开始query放入redis的数据总量
        dict_count = dict()
        for i in index_list:
            dict_count["count_" + i] = redis_cli.get("count_" + i).decode('utf8')

        start_time = datetime.now()
        # 根据关键字查找
        response = client.search(
            # 默认
            index=source,
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": fields
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
            hit_dict = dict()
            hit_dict["video_url"] = handle_null_data("video_url", hit["_source"])
            hit_dict["video_title"] = to_highlight("video_title", hit, hit_dict)
            hit_dict["director"] = handle_null_data("director", hit["_source"])
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
                                               "dict_count": dict_count,
                                               "topn_search": topn_search})


def handle_null_data(field_name, hit):
    if field_name in hit.keys():
        return hit[field_name]
    else:
        return "未爬取到"


def to_highlight(field_name, hit, hit_dict):
    if field_name in hit["highlight"]:
        return "".join(hit["highlight"][field_name])
    else:
        return handle_null_data(field_name, hit["_source"])

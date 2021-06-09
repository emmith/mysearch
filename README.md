#  视频搜索引擎
目前为测试版本，建议使用b站数据进行测试

已实现功能：
1. 热门搜索（搜索推荐）
2. 搜索补全  


## 本项目所使用工具
1. elastsearch 7.x
2. redis
3. django
4. kibana

## 运行说明
启动es、kibana、redis

用pycharm打开项目

在Spiders/bili下执行  
```scrapy crawl video_bili```  
在Spiders/dytt下执行   
```scrapy crawl video_dytt```    
dytt需要很多时间，建议爬取几百条强制结束

然后运行django项目


**如需采用更多搜索源，更改```views.py```文件中index的["video_bili","video_dytt"]列表即可，注意新的数据源必须和原来的数据源的字段名一致**

## 结果展示
结果所使用的数据源为dytt，即```views.py```文件中index为["video_dytt"]列表
### 首页
![](https://res.cloudinary.com/emmith/image/upload/v1623244073/marldown/%E9%A6%96%E9%A1%B5_l4qoi3.png)

### 搜索补全
![](https://res.cloudinary.com/emmith/image/upload/v1623244185/marldown/%E6%90%9C%E7%B4%A2%E8%A1%A5%E5%85%A8_oo5oh7.png)

### 搜索结果
![](https://res.cloudinary.com/emmith/image/upload/v1623244299/marldown/%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C_i0k3it.png)

## TO DO
* 须统一每个数据源的字段名
* 统一后，把其他数据源的spider导入

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from re import S
import scrapy


class BtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    referer = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 年代，如：2023
    year = scrapy.Field()
    # 又名
    alias = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 编剧
    writer = scrapy.Field()
    # 类型，如： 剧情 / 喜剧
    genre = scrapy.Field()
    # 地区，如： 中国大陆 / 美国
    region = scrapy.Field()
    # 语言
    language = scrapy.Field()
    # 片长
    runtime = scrapy.Field()
    # 豆 瓣:
    douban_rating = scrapy.Field()
    douban_url = scrapy.Field()
    # IMDb:
    imdb_rating = scrapy.Field()
    imdb_url = scrapy.Field()
    # 演员 A / 演员 B
    cast = scrapy.Field()
    # 剧情简介
    summary = scrapy.Field()
    
    #bt资源
    resource_name = scrapy.Field()
    #bt资源地址(magnet)
    resource_url = scrapy.Field()
    resource_remark = scrapy.Field()
    resource_category = scrapy.Field()
    resource_size = scrapy.Field()
    resource_count = scrapy.Field()
    resource_created_at = scrapy.Field()
    resource_srt_url = scrapy.Field()
    
    poster_url = scrapy.Field()
    still_url = scrapy.Field()
    poster_file = scrapy.Field()
    still_file = scrapy.Field()
    pass


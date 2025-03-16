# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediaItem(scrapy.Item):
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
    # 语言
    language = scrapy.Field()
    # 片长
    runtime = scrapy.Field()
    # 豆 瓣:
    douban_rating = scrapy.Field()
    # IMDb:
    imdb_rating = scrapy.Field()
    # 演员 A / 演员 B
    cast = scrapy.Field()
    # 剧情简介
    summary = scrapy.Field()
    pass

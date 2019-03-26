# -*- coding: utf-8 -*-
import scrapy
from movie.items import TencentItem
from movie import pipelines

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']
    pipeline = set([ pipelines.TencentPipeline ])
    def parse(self, response):
        print(".################..............parse...")
        for each in response.xpath('//*[@class="even"]'):
        
            item = TencentItem()
            print("##########", item)


            yield item

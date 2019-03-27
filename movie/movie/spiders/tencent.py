# -*- coding: utf-8 -*-
import scrapy
import re
from movie.items import TencentItem
from movie import pipelines


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=3068#a']
    pipeline = set([ pipelines.TencentPipeline ])
    def parse(self, response):
        print(".################..............parse...")
        tabletr = response.xpath('//table[@class="tablelist"]/tr[contains(@class,"even") or contains(@class,"odd")]')
        if len(tabletr) <=0:
            print("####### finished #####")
            return
        
        for each in tabletr:
        
            item = TencentItem()
            print("##########", item, each)
            c = each.xpath('./td/a/text()').extract_first()
            item['name'] = c

            
            yield item
        
        curpage = re.search('(\d+)',response.url).group(1)
        page = int( curpage ) + 10
        url = re.sub('\d+', str(page), response.url)
        print("###page###",curpage, url)
        yield scrapy.Request(url, callback = self.parse)

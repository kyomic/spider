#-*- coding: utf-8 -*-
import scrapy
from movie.items import MovieItem

class MeijuSpider(scrapy.Spider):
    name = 'meiju'
    allowed_domains = ['www.hpoi.net.cn']
    start_urls = ['http://www.hpoi.net.cn/hobby/all']

    def parse(self, response):
        print("~~~~~~...~~~parsing..\n")
        #movies = response.xpath('//div[@class="week-hot"]/ul/li')
        movies = response.xpath('//ul[contains(@class,"bs-glyphicons-list")]/li')
        print(movies)
        #pass
        for each_movie in movies:
            item = MovieItem()
            item['still'] = each_movie.xpath('./a/img/@src').extract_first()
            item['name'] = each_movie.xpath('./div//div[contains(@class,"hp-two-line")]/a/text()').extract_first()
            item['url'] = each_movie.xpath('./div//div[contains(@class,"hp-two-line")]/a/@href').extract_first()
            print("item.name==", item['name'])
            # call pipe
            yield item


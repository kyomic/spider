import scrapy


class MeijuSpider(scrapy.Spider):
    name = "meiju"
    allowed_domains = ["meijutt.tv"]
    start_urls = ["https://meijutt.tv"]

    def parse(self, response):
        pass

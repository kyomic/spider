import scrapy

class Bt66Spider(scrapy.Spider):
    name = "bt66"  # 这里的名称必须与命令中的 `bt66` 一致
    allowed_domains = ["bt66.org"]
    start_urls = ["https://bt66.org/news-type-id-9-type--area--year--order-addtime.html"]

    def start_requests(self):
        print("开始执行")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': 'ff_user=ZWtwbWNsWJqWzJudn8mi2F3QrtTPoclYzJ6dnMrKyM6kXZqdlpeZZpTIZ2pnnmqWn5tqypZwm2fJa2ZnncSZxWWbXZ6WnpqZmsaiq1qdmsqblW7Kx5mXmMqdZ2bKlZrDaG%2BbmmOYmm2XmGtulw%3D%3D'
        }
        # 发送请求并设置错误回调
        # meta={'handle_httpstatus_list': [302]} 表示允许的状态码列表
        yield scrapy.Request(url=self.start_urls[0], headers=headers, callback=self.parse, errback=self.errback_httpbin,  meta={'handle_httpstatus_list': [302]})

    def parse(self, response):
        # 解析逻辑
        print("执行结果response")
        list = response.css('.container .nopl').get()
        if list is None:
            print("没有数据")
            return
        if len(list) == 0:
            print("没有数据")
        print(list)
        pass

    def errback_httpbin(self, failure):
        print("执行结果failure")
        # 错误处理
        print(repr(failure))
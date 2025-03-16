import scrapy
from scrapy.selector import Selector
import re
from ..items import MediaItem

class VideoSpider(scrapy.Spider):
    name = "video"
    allowed_domains = ["4khdr.cn"]
    start_urls = ["https://4khdr.cn"]
    testing = True
    cur_page = 1
    max_page = 1

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.4khdr.cn/rank_7ree-rank_7ree.html'
        }
        # 发送请求并设置错误回调
        # meta={'handle_httpstatus_list': [302]} 表示允许的状态码列表
        yield scrapy.Request(url=self.start_urls[0], headers=headers, callback=self.parse, errback=self.errback_httpbin,  meta={'handle_httpstatus_list': [302]})
    def parse(self, response):
        print("执行结果response")
        list = response.css('.waterfall li').getall()
        if( self.max_page <= 1):
            self.max_page = self.get_max_page(response)
        self.max_page =2
        
        
        print("max_page", self.max_page)
        if self.testing:
            # 只获取第一个元素
            list = list[0:1]
            
        for item in list:
            selector = Selector(text=item)
            href = selector.css('a::attr(href)').get()
            if href:
                full_url = response.urljoin(href)
                media_item = MediaItem()
                media_item['referer'] = full_url
                print("a标签的href属性:", full_url)
                #yield media_item
                yield scrapy.Request(url=full_url, callback=self.parse_detail, errback=self.errback_httpbin,  meta={'handle_httpstatus_list': [302]})
            else:
                print("a标签没有href属性")
        
        # if( self.cur_page <= self.max_page):
        #     self.cur_page = self.cur_page + 1
        #     next_page = self.get_page_url( self.cur_page )
        #     yield scrapy.Request(url=next_page, callback=self.parse, errback=self.errback_httpbin,  meta={'handle_httpstatus_list': [302]})
        # if list is None:
        #     print("没有数据")
        #     return

    
    def parse_detail( self, response):
         # 从 meta 中取出 media_item
        media_item = response.meta.get('media_item')
        print("执行结果response")
        root = response.css('.t_fsz')
        html_content = root.css('td').get()
        pattern = r'<strong>(.*?)</strong>(.*?)<br>'
        matches = re.findall(pattern, html_content, re.DOTALL)
        for match in matches:
            print(f"标签内容: {match[0].strip()}")
            print(f"匹配内容: {match[1].strip()}")
            print()
        
        try:
            cast_pattern = r'<strong>主演名单</strong><br>(.*?)<br>'
            cast = re.findall(cast_pattern, html_content, re.DOTALL)
            summary_pattern = r'<strong>剧情简介</strong><br>(.*?)<br>'
            summary = re.findall(summary_pattern, html_content, re.DOTALL)
            
            media_item['cast'] = cast[0].strip()
            media_item['summary'] = summary[0].strip()
            yield media_item
        except Exception as e:
            print("解析失败", e)
        
        


    def get_page_url(self, page ):
        return f'https://www.4khdr.cn/forum-2-{page}.html'
    
    def get_max_page(self, response):
        max_page = response.css('#fd_page_bottom a.last::text').get()
        max_page = re.sub(r'\D', '', max_page)
        print("max_page", max_page)
        return max_page
    
    
    def errback_httpbin(self, failure):
        print("执行结果failure")
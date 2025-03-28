import scrapy
import sys
import os
import re
import csv
from scrapy.selector import Selector
# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取父目录
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
parent_dir = os.path.dirname(parent_dir)
print("父目录路径：", parent_dir)
# 将父目录添加到 sys.path 中
sys.path.append(parent_dir)
from session.login import Loginable
from core.pageable import Pageable

from ..items import BtItem
class Bt66Spider(Loginable, Pageable, scrapy.Spider):
    name = "bt66"  # 这里的名称必须与命令中的 `bt66` 一致
    #allowed_domains = ["bt66.org"]
    start_urls = ["https://0067.org/news-type-id-9-type--area--year--order-addtime.html"]
    session = {}
    existing_referers = {}
    def __init__(self):
        super().__init__()  # 调用 Spider 的 __init__
        super(Loginable, self).__init__()  # 调用 Loginable 的 __init__
        super(Pageable, self).__init__()  # 调用 Pageable 的 __init__
        
        session = self.check_login()
        
    def config_login(self):
        print("配置登录Parent")
        # return {
        #     'url': 'https://0067.org/user-loginpost.html',
        #     'method': 'POST',
        #     'data': {
        #         'user_email':'rian@qq.com',
        #         'user_pwd':'1qaz1qaz',
        #         'user_vcode':{
        #             'type':'input',
        #             'url': 'https://0067.org/index.php?s=Vcode-Index',
        #             'name':'验证码',
        #         },
        #         'user_remember':1
        #     },
        # }
        return {
            'url': 'https://0067.org/user-loginpost.html',
            'method': 'POST',
            'data': {
                'user_email':'kyomic@163.com',
                'user_pwd':'1qaz1qaz',
                'user_vcode':{
                    'type':'input',
                    'url': 'https://0067.org/index.php?s=Vcode-Index',
                    'name':'验证码',
                },
                'user_remember':1
            },
        }
        
    
    def generate_headers(self):
        return  {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            
            #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            #'Accept-Encoding':'gzip, deflate, br',
            #'Cache-Control':'no-cache',
            #'Connection':'keep-alive',
            #'Host':'0067.org',
            #'Referer': 'https://0067.org/user-center-action-index.html',
            #'Cookie': self.session['cookie']
            "Cookie":  self.session['cookie']
        }
    
    def generate_request(self, url, onsuccess=None, onerror=None, meta=None):
       return scrapy.Request(url=url, cookies=self.get_cookies(), method='GET',headers=self.generate_headers(), callback=onsuccess, errback=onerror, meta=meta)
        
    def start_requests(self):
        print("开始请求2:当前页", self.cur_page, self.start_urls[0])
        print("cookie", self.session['cookie'])
        print("cookies", self.get_cookies())
        # 发送请求并设置错误回调
        # meta={'handle_httpstatus_list': [302]} 表示允许的状态码列表
        # 坑，headers的cookie没用，要用 cookies参数
        #yield scrapy.Request(url=self.start_urls[0], cookies=self.get_cookies(), method='GET',headers=self.generate_headers(), callback=self.parse, errback=self.errback_httpbin, meta={'handle_httpstatus_list': [302]})
        yield self.generate_request(self.start_urls[0], self.parse, self.errback_httpbin, meta={'handle_httpstatus_list': [302]})

    def parse_max_page(self, response):
        print("解析最大页码")
        print(response.text)
        list = response.css('ul.pagination li.page-item').getall()
        if list is None:
            print("没有最大数据")
            print(response.text)
            return 1
        
        def get_number_from_string(item):
            # 使用正则表达式匹配字符串中的数字
            selector = Selector(text=item)
            page = selector.css('a.page-link::text').get()
            page = page.replace('.', '')
            try:
                page_int = int(page)
                is_valid_number = True
            except ValueError:
                is_valid_number = False
                
            if is_valid_number:
                return page_int
            return 1
        
        page_number = get_number_from_string(list[-1])
        if page_number >1:
            return page_number
        else:
            page_number = get_number_from_string(list[-2])
        
        return page_number

    def get_page_url(self, page):
        return f'https://0067.org/news-type-id-9-type--area--year--order-addtime-p-{page}.html'
    
    def is_exist_referer(self, referer):
        # 检查 referer 是否存在于 existing_referers 集合中
         # 读取 items.csv 文件
        
        exist = False
        
        try:
            with open('items.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('referer')==referer and row.get('resource_url'):
                        self.existing_referers[row['referer']] = row['referer']
                        exist = True
        except FileNotFoundError:
            pass
        return exist
    def parse(self, response):
        # 解析逻辑
        list = response.css('table.data tr').getall()
        print('当前页：',self.cur_page, '最大页：',self.max_page, '当前页url：',response.url)
        if self.max_page < 1:
            self.max_page = self.get_max_page(response)
            print('最大页：',self.max_page)
        
        if self.testing:
            self.max_page = self.cur_page
            list = list[0:2]
            
        for item in list:
            selector = Selector(text=item)
            has_even_or_odd = bool(selector.css('.even, .odd'))
            if not has_even_or_odd:
                continue
            href = response.urljoin(selector.css('td a::attr(href)').get())
            if( self.is_exist_referer(href) ):
                print("referer已存在", href)
                continue
            resource_name = selector.css('a.ico::text').get()
            img = response.urljoin(selector.css('img::attr(data-original)').get())
            title = selector.get()+''
            # 查找 <br> 和 </td> 之间的内容
            td_content = re.findall(r'<br>(.*?)</td>', item, re.DOTALL)
            if td_content is not None and len(td_content) > 0:
                title = td_content[0].strip()
            else:
                title = None
            #print("a标签的href属性:", href, resource_name, img, title )
            
            media_item = BtItem()
            media_item['referer'] = href
            media_item['poster_url'] = img
            media_item['resource_name'] = title
            media_item['resource_remark'] = td_content
            
            yield self.generate_request(href, self.parse_detail, self.errback_httpbin, meta={'media_item':media_item, 'handle_httpstatus_list': [302]})
       
        if( self.cur_page < self.max_page):
            self.cur_page = self.cur_page + 1
            next_page = self.get_page_url( self.cur_page )
            #yield scrapy.Request(url=next_page, cookies=self.get_cookies(), headers=headers, callback=self.parse, errback=self.errback_httpbin,  meta={'handle_httpstatus_list': [302]})
            yield self.generate_request(next_page, self.parse, self.errback_httpbin, meta={'handle_httpstatus_list': [302]})
        if list is None:
            print("没有数据")
            return
        pass
    
    def mapToKey(self, name):
        name = name.replace(" ", "")
        map = {
            "title":"名称|Title",
            "year":"年代|Year",
            "alias":"又名|别名",
            "director":"导演|Director",
            "writer":"编剧",
            "genre":"类型",
            "region":"制片国家|地区",
            "language":"语言",
            "runtime":"片长|Runtime",
            "douban_rating":"豆瓣|豆瓣评分|豆瓣分",
            "imdb_rating":"IMDb评分|imdb|IMDB Rating",
            "cast":"主演|Actors",
            "summary":"剧情简介|Plot",
            "referer":"来源",
            "resource_category":"Category",
            "resource_size":"Size",
            "resource_count":"Files",
            "resource_created_at":"Added",
        }
        for key in map:
            pattern = map[key]
            arr=pattern.split("|")
            for i in range(len(arr)):
                arr[i] = arr[i].strip()
                if re.search(arr[i], name):
                    return key
        return ""
    
    def parse_detail(self, response):
        # 解析逻辑
        print("执行结果response")
        media_item = response.meta['media_item']
        root_detail = response.css('ul.detail li').getall()
        for item in root_detail:
            selector = Selector(text=item)
            name = selector.css('strong::text').get()
            name = name.replace(":", "")
            value = selector.css('div::text').get()
            key = self.mapToKey(name)
            if key == "":
                continue
            if key =='imdb_rating':
                key = 'imdb_url'
                value = selector.css('a::attr(href)').get()
            media_item[key] = value
        
        root_tree = response.css('ul.fileTree li').getall()
        for item in root_tree:
            ele = Selector(text=item)
            content = ele.get()+''
            splits = content.split(":")
            if len(splits) < 2:
                continue
            name = splits[0].strip()
            key = self.mapToKey(name)
            value = splits[1].strip()
            value = re.sub(r'<[^>]*>', '', value)
            if key == "":
                continue
            if key=='douban_rating':
                val = ele.css("a::attr(href)").get()
                if val is not None:
                    value = val
                    key = 'douban_url'
                
            media_item[key] = value
            print(key, value)
        
        root_down = response.css('div.tdown')
        magnet = root_down.css('a.btn-primary::attr(href)').get()
        srt = root_down.css('a.btn-warning::attr(href)').get()
       
        media_item['resource_url'] = magnet
        media_item['resource_srt_url'] = response.urljoin(srt)
        if( magnet is None or magnet == "javascript:void(0);"):
            print("没有数据")
            # 退出程序,关闭Spider
            self.crawler.engine.close_spider(self, 'No data')
            
            return
        yield media_item
        #yield scrapy.Request(url=response.urljoin(src), callback=self.save_image, meta={'path': path})
        

    def errback_httpbin(self, failure):
        print("执行结果failure")
        # 错误处理
        print(repr(failure))

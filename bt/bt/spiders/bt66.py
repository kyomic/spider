import scrapy
import sys
import os
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

class Bt66Spider(Loginable,scrapy.Spider):
    name = "bt66"  # 这里的名称必须与命令中的 `bt66` 一致
    allowed_domains = ["bt66.org"]
    start_urls = ["https://bt66.org/news-type-id-9-type--area--year--order-addtime.html"]
    def __init__(self):
        super().__init__()  # 调用 Spider 的 __init__
        super(Loginable, self).__init__()  # 调用 Loginable 的 __init__
        
        self.check_login()
        
    def config_login(self):
        print("配置登录")
        return {
            'url': 'https://bt66.org/user-loginpost.html',
            'method': 'POST',
            'data': {
                'user_email': {
                    'type': 'input',
                    'name': '用户名',
                },
                'user_pwd': {
                    'type': 'input',
                    'name': '密码',
                },
                'user_vcode': {
                    'type': 'qrcode',
                    'url': 'https://bt66.org/index.php?s=Vcode-Index',
                    'name': '验证码',
                },
                'user_remember':1
            },
        }
        
    def start_requests(self):
        
       
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
from urllib import response
import scrapy
import requests
from PIL import Image
import pytesseract  # pip install pillow pytesseract tesseract
from io import BytesIO

from urllib.parse import urlencode
class Loginable(scrapy.Spider):
    def __init__(self):
        print('init Loginable')
        #input('请输入用户名:')

    def login(self, username, password):
        return True
    
    def config_login(self):
        return {
            'url': 'https://bt66.org/user-loginpost.html',
            'method': 'POST',
            'data': {
                'user_email':'riacn@qq.com',
                'user_pwd':'1qaz1qaz',
                'user_vcode':{
                    'type':'qrcode',
                    'url': 'https://bt66.org/index.php?s=Vcode-Index',
                    'name':'验证码',
                },
                'user_remember':1
            },
        }

    def check_login(self):
        try:
            # raise Exception("config is None, please check config_login")
            
            config = self.config_login()
            if config is None:
                raise Exception("config is None, please check config_login")

            params = config['data']
            for key, value in params.items():
                if isinstance(value, dict):
                    print('kiey',key)
                    sub_name = value.get('name')
                    sub_value = value.get('value')  # 使用 get 方法避免 KeyError
                    sub_type = value.get('type')
                    sub_url = value.get('url')
                    if sub_type == 'input':
                        if sub_name:
                            user_input = input('请输入' + sub_name + '('+ key +'):')
                            params[key] = user_input
                    if sub_type == 'qrcode':
                        if sub_url is None:
                            raise Exception("sub_url is None, please check config_login")
                        
                        response = requests.get(sub_url)
                        response.raise_for_status()
                        # 打开图片
                        image = Image.open(BytesIO(response.content))
                        download_path = "downloaded_image.jpg"
                        image.save(download_path)
                        print(f"图片已下载到 {download_path}")
                        user_input = input('请输入' + sub_name + '('+ key +'):')
                        params[key] = user_input

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Cookie': 'ff_user=ZWtwbWNsWJqWzJudn8mi2F3QrtTPoclYzJ6dnMrKyM6kXZqdlpeZZpTIZ2pnnmqWn5tqypZwm2fJa2ZnncSZxWWbXZ6WnpqZmsaiq1qdmsqblW7Kx5mXmMqdZ2bKlZrDaG%2BbmmOYmm2XmGtulw%3D%3D'
            }
            response = requests.post(
                url=config['url'],
                data=urlencode(config['data']).encode('utf-8'), 
            )
            json = response.json()
            print('response',json)
            if( response.status_code !=200):
                print('登录失败', json.info)
                return
        except Exception as e:
            print(f"执行 check_login 时出错: {e}")
   
    def after_login(self, response):
        print('登录成功', response)
        pass

    def errback_httpbin(self, failure):
        print("执行结果failure")
        # 错误处理
        print(repr(failure))

class Test(Loginable):
    def __init__(self):
        super().__init__()  # 调用 Loginable 的 __init__
        print('准备登录')

class Abc():
    def __init__(self):
        super().__init__()  # 调用 Loginable 的 __init
        
        config = {
            'url': 'https://bt66.org/user-loginpost.html',
            'method': 'POST',
            'data': {
                'user_email':'riacn@qq.com',
                'user_pwd':'1qaz1qaz',
                'user_vcode':{
                    'type':'qrcode',
                    'url': 'https://bt66.org/index.php?s=Vcode-Index',
                    'name':'验证码',
                },
                'user_remember':1
            },
        }
        
        print('REQUEST',config)
        # scrapy.Request(
        #     url=config['url'],
        #     method=config['method'],
        #     body=urlencode(config['data']).encode('utf-8'),
        #     #callback=self.after_login,
        #     errback=self.errback_httpbin,
        #     meta={'handle_httpstatus_list': [302]}
        # )
        response = requests.post(
            url=config['url'],
            data=urlencode(config['data']).encode('utf-8'), 
        )
        print('response',response.text)
        
    
    def after_login(self, response):
        print('登录成功', response)
        pass

    def errback_httpbin(self, failure):
        print("执行结果failure")
        # 错误处理
        print(repr(failure))
        
        
if __name__ == '__main__':
    instance = Test()
    # 由于 check_login 是生成器，需要使用 for 循环或 next 函数来获取结果
    params = instance.check_login()
    
    
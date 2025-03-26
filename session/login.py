from urllib import response
import scrapy
import requests
import os
import json
import re
from PIL import Image
#import pytesseract  # pip install pillow pytesseract tesseract
from io import BytesIO

from urllib.parse import urlencode
class Loginable(scrapy.Spider):
    session = {}
    # 是否缓存session
    cache_session = True
    cookie_parts = []
    def __init__(self):
        print('init Loginable')
        #self.logout()
        #input('请输入用户名:')

    def generate_useragent(self):
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    
    def get_session_file_name(self):
        return '0067.org.session'
    
    
    def login(self, username, password):
        return True
    
    
    def parse_cookie_str( self, str ):
        cookies = str.split(';')
        # 提取每个 cookie 的 key=value 部分
        for cookie in cookies:
            # 按分号分割，取第一个部分即 key=value
            cookie = re.sub(r'path=/,', '', cookie)
            key_value = cookie.strip()
            # 检查是否包含 '='，如果不包含则跳过
            if '=' not in key_value:
                continue
            # 按等号分割，取第一个部分即 key
            key = key_value.split('=')[0]
            value = key_value.split('=')[1]
            # 检查 key 是否为 'expires' 或 'Max-Age'，如果是则跳过
            if key in ['expires', 'Max-Age', 'path']:
                continue
            # 查找 cookie_parts 中是否已经存在该 key
            found = False
            for c in self.cookie_parts:
                if c.get('name') == key:
                    # 如果存在，更新该 key 对应的值
                    c['value'] = value
                    found = True
                    break
            # 如果不存在，添加新的 key-value 对
            if not found:
                self.cookie_parts.append({'name': key, 'value':value})
            # 否则将 key=value 添加到结果列表
        # 重新组合成字符串
        return self.cookie_parts
    
    def has_cookie(self, name):
        found = False
        for c in self.cookie_parts:
            if c.get('name') == name:
                found = True
                break
        return found
    def get_cookie_value(self, name):
        for c in self.cookie_parts:
            if c.get('name') == name:
                return c.get('value')
        return None

    def update_cookie(self, response):
        str = response.headers['Set-Cookie']
        self.parse_cookie_str(str)
    
    def get_cookie(self):
        """
        获取拼接后的 cookie 字符串。
        该方法会检查 self.cookie_parts 是否为 None，如果是则将其初始化为空列表，
        然后将 self.cookie_parts 中的每个字典元素的 'value' 字段值提取出来，
        并使用分号 ';' 连接成一个字符串返回。
    
        :return: 拼接后的 cookie 字符串
        """
        # 检查 self.cookie_parts 是否为 None，如果是则初始化为空列表
        if self.cookie_parts is None:
            self.cookie_parts = []
        
        return  ';'.join([f"{item['name']}={item['value']}" for item in self.cookie_parts])
    
    def get_cookies( self ):
        cookies = []
        for item in self.cookie_parts:
            cookies.append({'name': item['name'], 'value': item['value']})
        return cookies
            
    def load_session( self ):
        filename = self.get_session_file_name()
        if os.path.exists(filename) and self.cache_session:
            print('session file exists')
            filename = self.get_session_file_name()
            try:
                with open(filename, 'r') as file:
                    self.session = json.load(file)
                
                cookie = self.session['cookie']
                
                if cookie is not None:
                    self.parse_cookie_str(cookie)
                
                print(f"Session 数据已成功从 {filename} 读取")
            except Exception as e:
                print(f"读取文件时出错: {e}")
                
    def init_session(self):
        filename = self.get_session_file_name()
        if os.path.exists(filename) and self.cache_session:
            self.load_session()
        else:
            print('session file not exists')
            print('获取Token')
            try:
                response = requests.get(
                    url='https://0067.org/user-login.html',
                    headers={
                        'User-Agent': self.generate_useragent(),
                        'Cookie': self.get_cookie()
                    }
                )
                response.raise_for_status()
                self.update_cookie(response)
                print('获取Token成功')

            except Exception as e:
                print(f"获取Token时出错: {e}")
                return
            try:
                response_qrcode = requests.get(
                    url='https://0067.org/index.php?s=Vcode-Index',
                    headers={
                        'User-Agent': self.generate_useragent(),
                        #'Cookie': self.get_cookie()
                    } 
                )
                response_qrcode.raise_for_status()
                self.update_cookie(response_qrcode)
                image = Image.open(BytesIO(response_qrcode.content))
                download_path = "downloaded_image.jpg"
                image.save(download_path)
                print(f"图片已下载到 {download_path}")
            except Exception as e:
                return
            
    
        self.flush_cookie()
        print('session:', self.session)
        return self.session

        
    def flush_cookie(self):
        self.session['cookie'] =  self.get_cookie()
        filename = self.get_session_file_name()
        try:
            with open(filename, 'w') as file:
                json.dump(self.session, file, indent=4)
            print(f"Session 数据已成功以 JSON 格式写入 {filename}")
        except Exception as e:
            print(f"写入文件时出错: {e}")


    def config_login(self):
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
        return {
            'url': 'https://0067.org/user-loginpost.html',
            'method': 'POST',
            'data': {
                'user_email':'riacn@qq.com',
                'user_pwd':'1qaz1qaz',
                'user_vcode':{
                    'type':'input',
                    'url': 'https://0067.org/index.php?s=Vcode-Index',
                    'name':'验证码',
                },
                'user_remember':1
            },
        }

    def logout(self):
        self.load_session()
        response = requests.get(
            url='https://0067.org/user-logout.html',
            headers={
                'User-Agent': self.generate_useragent(),
                'Cookie': self.get_cookie()
            }
        )
        print('退出登录', response.headers)
    def check_login(self):
        print('检查登录')
        session = self.init_session()
        user_cookie = self.get_cookie_value('ff_user')
        if user_cookie is not None:
            print('已登录')
            return self.session
        else:
            print('未登录，准备登录')
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
                            
                            php_session_id_cookie = [cookie for cookie in self.session_cookies if 'PHPSESSID' in cookie]
                            print('php session', php_session_id_cookie)
                            response = requests.get(sub_url, headers={
                                'User-Agent': self.generate_useragent(),
                                #'Cookie': '; '.join(php_session_id_cookie)
                            })
                            print("会话cookie:", session, response.headers)
                            response.raise_for_status()
                            
                            # 打开图片
                            image = Image.open(BytesIO(response.content))
                            download_path = "downloaded_image.jpg"
                            image.save(download_path)
                            print(f"图片已下载到 {download_path}")
                            user_input = input('请输入' + sub_name + '('+ key +'):')
                            params[key] = user_input

                headers = {
                    'User-Agent': self.generate_useragent(),
                    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                    #'Origin':'https://0067.org',
                    #'Referer':'https://0067.org/user-login.html',
                    'Cookie': self.get_cookie()
                }
                print('请求:', config['url'])
                print('请求头:', headers)
                response = requests.post(
                    url=config['url'],
                    headers=headers,
                    data=urlencode(config['data']).encode('utf-8'), 
                )
                json = response.json()
                respnse_header = response.headers
                print('response',json)
                print('响应头:',respnse_header)
                self.logout()
                if( response.status_code !=200):
                    print('登录失败', json.info)
                    return
                if json and json['data'] == 0:
                    print('登录失败', json['info'])
                    self.logout()
                    return
                    
                self.update_cookie(response)
                self.flush_cookie()
            except Exception as e:
                print(f"执行 check_login 时出错: {e}")
        
        return self.session
   
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
            'url': 'https://0067.org/user-login.html',
            'method': 'POST',
            'data': {
                'user_email':'riacn@qq.com',
                'user_pwd':'1qaz1qaz',
                'user_vcode':{
                    'type':'qrcode',
                    'url': 'https://0067.org/index.php?s=Vcode-Index',
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
    session = instance.check_login()
    print('会话数据:',session)
    
    
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
class Pageable(scrapy.Spider):
    cur_page = 24
    max_page = -1
    # 开启测试模式，直接获取第一页，第一条数据
    testing = False
    def get_max_page(self, response):
        return self.parse_max_page(response)
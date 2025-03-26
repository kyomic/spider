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
    cur_page = 1
    max_page = -1
    testing = False
    def get_max_page(self, response):
        return self.parse_max_page(response)
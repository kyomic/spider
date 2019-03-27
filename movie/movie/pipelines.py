# -*- coding: utf-8 -*-
# encoding=utf8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from scrapy import log
import functools

def check_spider_pipeline(process_item_method):

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # message template for debugging
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)

        # if class is in the spider's pipeline, then use the
        # process_item method normally.
        if self.__class__ in spider.pipeline:
            spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)

        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
            spider.log(msg % 'skipping', level=log.DEBUG)
            return item

    return wrapper

class MoviePipeline(object):
    @check_spider_pipeline
    def process_item(self, item, spider):
        print("movie pipe is call......................")
        return item
        with open("my_meiju.txt","a") as fp:
            fp.write("############################\n")
            fp.write(item['name'].encode('utf8')+"\n")
            fp.write(item['still'].encode('utf8') + "\n")

            fp.write("LINK:"+item['url'].encode('utf8') + "\n")
        return item


class TencentPipeline(object):
    @check_spider_pipeline
    def process_item(self, item, spider):
         print("TecentPipe is called................."+ item['name'])
         with open("tencent_job.txt","a") as fp:
            fp.write("###########################\n")
            fp.write(item['name'].encode('utf8')+"\n")
         return item
         return item

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class MediaPipeline:
    def process_item(self, item, spider):
        return item




class CsvWriterPipeline:
    def open_spider(self, spider):
        # 打开 CSV 文件
        self.file = open('items.csv', 'w', newline='', encoding='utf-8')
        # 创建 CSV 写入器，使用更新后的 fieldnames
        self.writer = csv.DictWriter(self.file, fieldnames=spider.settings.get('CSV_FIELDS', []))
        # 写入 CSV 文件的表头
        self.writer.writeheader()

    def close_spider(self, spider):
        # 关闭 CSV 文件
        self.file.close()

    def process_item(self, item, spider):
        # 将 Item 数据写入 CSV 文件
        self.writer.writerow(item)
        return item
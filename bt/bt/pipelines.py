# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os
from scrapy.exporters import CsvItemExporter

class BtPipeline:
    def process_item(self, item, spider):
        return item


class CsvWriterPipeline:
    def open_spider(self, spider):
        # 检查 items.csv 文件是否存在
        
        self.existing_referers = set()
        if os.path.exists('items.csv'):
            f = open('items.csv', 'r', encoding='utf-8-sig')
            try:
                reader = csv.DictReader(f)
                for row in reader:
                    referer = row.get('referer')
                    if referer:
                        self.existing_referers.add(referer)
            finally:
                f.close()
        # 打开 CSV 文件
        self.file = open('items.csv', 'a', newline='', encoding='utf-8-sig')
        # 创建 CSV 写入器，使用更新后的 fieldnames，并设置 quoting 参数为 csv.QUOTE_ALL
        self.writer = csv.DictWriter(self.file, fieldnames=spider.settings.get('CSV_FIELDS', []), quoting=csv.QUOTE_ALL)
        # 如果文件为空，写入 CSV 文件的表头
        if os.path.getsize('items.csv') == 0:
            self.writer.writeheader()

    def close_spider(self, spider):
        # 关闭 CSV 文件
        self.file.close()

    def process_item(self, item, spider):
        referer = item.get('referer')
        if referer and referer in self.existing_referers:
            # 如果 referer 已存在，不再发送请求
            print(f"Referer {referer} already exists, skipping request.")
            return None
        else:
            if referer:
                self.existing_referers.add(referer)
            # 将 Item 数据写入 CSV 文件
            self.writer.writerow(item)
            return item
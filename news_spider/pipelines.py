# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import news_spider.spiders.ithome_spider

class NewsSpiderPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def open_spider(self, spider):
        # 在爬虫开启时建立数据库连接
        self.conn = mysql.connector.connect(
            host=spider.settings.get('MYSQL_HOST'),
            database=spider.settings.get('MYSQL_DATABASE'),
            user=spider.settings.get('MYSQL_USER'),
            passwd=spider.settings.get('MYSQL_PASSWORD'),
            port=spider.settings.get('MYSQL_PORT'),
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        # 在爬虫关闭时断开连接
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        # 将每个item存入数据库
        sql = "INSERT INTO news (title, url, time, tag,origin) VALUES (%s, %s, %s, %s, %s)"
        values = (
            item.get('title'),
            item.get('url'),
            item.get('time'),
            ', '.join(item.get('tag', [])),
            item.get('origin')
        )
        self.cursor.execute(sql, values)
        self.conn.commit()
        return item


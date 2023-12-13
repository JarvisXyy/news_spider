# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    time = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    comment = scrapy.Field()
    picture = scrapy.Field()
    tag = scrapy.Field()
    origin = scrapy.Field() # 来源网站
    brief = scrapy.Field() # 简介

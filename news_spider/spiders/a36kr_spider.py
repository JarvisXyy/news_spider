import scrapy


class A36krSpiderSpider(scrapy.Spider):
    name = "36kr_spider"
    allowed_domains = ["36kr.com"]
    start_urls = ["https://36kr.com/information/travel"]

    def parse(self, response):
        pass

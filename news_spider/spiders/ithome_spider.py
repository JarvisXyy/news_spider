import json
import datetime
from datetime import datetime
import scrapy
from news_spider.items import NewsSpiderItem


class IthomeSpiderSpider(scrapy.Spider):
    name = "ithome_spider"
    allowed_domains = ["auto.ithome.com"]
    start_urls = ["https://auto.ithome.com"]

    def parse(self, response):
        # 实例化一个item对象
        item = NewsSpiderItem()
        count = 0
        if isinstance(response, scrapy.http.response.html.HtmlResponse):
            # 定位到包含所有新闻项的容器
            news_list = response.xpath('//*[@id="list"]/div[1]/ul/li')
            # 遍历每一项新闻
            for news in news_list:
                # 提取每个新闻项的具体信息
                item['title'] = news.xpath('.//div/h2/a/@title').extract()[0]
                item['url'] = news.xpath('.//div/h2/a/@href').extract()[0]
                item['time'] = news.xpath('.//div/@data-ot').extract()[0]
                item['tag'] = news.xpath('.//div/a/text()').extract()
                yield item

            last_news_time_xpath = f'//*[@id="list"]/div[1]/ul/li[30]/div/@data-ot'
            last_news_time = response.xpath(last_news_time_xpath).get()
            last_news_timestamp = datetime.strptime(last_news_time, '%Y/%m/%d %H:%M:%S').timestamp()
            next_url = 'https://auto.ithome.com/category/domainpage?domain=auto&subdomain=&ot=' + str(
                int(last_news_timestamp)) + '000'
            yield scrapy.Request(next_url, meta={'count': count, 'item': item}, method='POST', callback=self.parse)

        else:
            # 如果不是HTML响应，则将响应转换为JSON对象
            data = json.loads(response.text)
            if data.get('success'):
                # 获取新闻列表
                new_html = data['content']['html']
                # 将HTML转换为Selector对象
                html = scrapy.Selector(text=new_html)
                # 处理新加载的新闻
                news_list = html.xpath('//li')
                for news in news_list:
                    item['title'] = news.xpath('.//div/h2/a/@title').extract()[0]
                    item['url'] = news.xpath('.//div/h2/a/@href').extract()[0]
                    item['time'] = news.xpath('.//div/@data-ot').extract()[0]
                    item['tag'] = news.xpath('.//div/a/text()').extract()
                    yield item
                    count += 1
                if count % 30 == 0 and item[
                    'title'] != '车评人韩路爆料小米汽车信息：定位 C 级豪华，售价超 30 万 / 高配近 40 万':
                    last_news_time = item['time']
                    print(item['time'])
                    print(item['title'])
                    last_news_timestamp = datetime.strptime(last_news_time, '%Y/%m/%d %H:%M:%S').timestamp()
                    next_url = 'https://auto.ithome.com/category/domainpage?domain=auto&subdomain=&ot=' + str(
                        int(last_news_timestamp)) + '000'
                    yield scrapy.Request(next_url, meta={'item': item}, method='POST',
                                         callback=self.parse)
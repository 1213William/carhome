# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

"""
1、首先需要对这个URL进行循环遍历，得到所有的网页的URL
2、对URL进行操作，得到里面的内容
"""


class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/price/brand-1.html']

    def parse(self, response):
        sel = Selector(response)
        yield scrapy.Request(response.url, callback=self.parse_url)
        next_url = sel.xpath('//div[@class="page"]/a[@class="page-item-next"]/@href').extract_first()
        if next_url:
            cmp_url = 'https://car.autohome.com.cn' + next_url

            yield scrapy.Request(cmp_url, callback=self.parse, dont_filter=True)
        # yield scrapy

    def parse_url(self, response):
        sel = Selector(response)
        for data in sel.xpath('//div[@class="list-cont"]'):
            title = data.xpath('div/div[2]/div[1]/a/text()').extract_first()
            price = data.xpath('div/div[2]/div[2]/div[2]/div[1]/span/span/text()').extract_first()
            print(title, price)


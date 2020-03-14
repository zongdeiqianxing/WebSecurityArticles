# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        print(response, response.url, "---------------------")

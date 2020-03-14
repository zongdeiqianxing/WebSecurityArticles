# -*- coding: utf-8 -*-
import scrapy


class Hao24Spider(scrapy.Spider):
    name = "hao24"
    allowed_domains = ["hao24.com"]
    start_urls = ['https://hao24.com/']

    def parse(self, response):
        print(response,response.url,"---------------------")

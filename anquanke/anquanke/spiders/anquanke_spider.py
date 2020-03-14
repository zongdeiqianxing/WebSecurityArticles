# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from anquanke.items import AnquankeItem
import json
import re

class AnquankeSpiderSpider(scrapy.Spider):
    name = "anquanke_spider"
    allowed_domains = ["anquanke.com"]
    # 安全资讯 安全知识 安全热点招聘 安全活动 每日安全热点 网络安全热点漏洞分析 恶意软件 活动 CTF Web安全 安全漏洞 漏洞 安全研究 技术分析 系统安全 渗透测试 漏洞预警代码审计
    start_urls = ['https://api.anquanke.com/data/v1/posts?size=10&page=1&tag=Web%E5%AE%89%E5%85%A8',]

    def start_requests(self):
        tags=['Web安全','渗透测试','安全知识',]
        for tag in tags:
             url = r'https://api.anquanke.com/data/v1/posts?size=10&page=1'r'&tag='+tag
             yield scrapy.Request(url,callback=self.parse)


    def parse(self, response):
        item={}
        resp = json.loads(response.text)
        if resp.get('success') != 'true':
            pass
        for i in range(0, 10):
            if resp.get('data')[i] is not None:
                item['readNum']=resp.get('data')[i].get('pv')
                if int(item['readNum']) < 200000:
                    continue
                item['title'] = resp.get('data')[i].get('title')
                if "招聘" in item['title'] or "offer" in item['title']:
                    continue
                item['url'] = r"https://anquanke.com/post/id/"+str(resp.get('data')[i].get('id'))
                yield item
            else:
                continue
                #self.crawler.engine.close_spider(self, '数据为空，停止爬虫!')

        if resp.get('next') is not None:
            next_page = resp.get('next').replace('\\','')
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            pass


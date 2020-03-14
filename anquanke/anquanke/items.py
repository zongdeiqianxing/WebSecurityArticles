# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnquankeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    readNum = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    #date = scrapy.Field()


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt
import time

class AnquankePipeline(object):
    def __init__(self):
        date = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        self.filename='Article'+date+'.md'
        # with open(self.filename,'w+') as f:
        #     f.write("#### 安全客高阅读(大于50w)资料")
        #     f.write('\n')

    def write_md(self,filename,str_row):
        with open(filename,'a+') as f:
            f.write(str_row+'  \r')
            #f.write('\n')

    def process_item(self, item, spider):
        readNum = int(item.get('readNum'))
        str_row = r"[【" + str(item.get('readNum'))[:-4] + 'w】  /' + item.get('title') + r"](" + item.get('url') + r")"
        if 200000 < readNum < 500000:
            self.write_md("20w+"+self.filename,str_row)
        elif 500000 < readNum < 800000:
            self.write_md("50w+" + self.filename,str_row)
        elif 800000 < readNum:
            self.write_md("80w+" + self.filename,str_row)



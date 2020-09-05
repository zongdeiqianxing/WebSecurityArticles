#coding:utf-8
import requests,time
from lxml import etree

base_url=r"http://xz.aliyun.com/?page="				
list=[]
headers = {
    'User-Agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13',
}

def write_md():
	date = time.strftime("%Y%m%d", time.localtime())
	filename="xianzhi-all-" + date + '.md'
	with open(filename,'a+') as f:
		for line in list:
			f.write(line)

def main():	
	try:
		for n in range(1,1000):
			url=base_url+str(n)
			print("正在读取："+url)
			result = requests.get(url=url,headers=headers).text
			#print(result)
			if '页面找不到了' in result:
				write_md()
				exit("已爬完-_-")

			tree = etree.HTML(result)
			xpath=tree.xpath(r'//div[@id="includeList"]/table/tr/td')
			print(xpath)
			if xpath is None:
				write_md()
				exit("出错-_-")
				
			
			for i in xpath:
				i=etree.HTML(etree.tostring(i).decode('utf-8'))
				comments =''.join(i.xpath(r'//p[@class="topic-info"]/span/span/text()')).strip()
				#print(comments)
				title=''.join(i.xpath(r'//p[@class="topic-summary"]/a/text()')).strip()
				href=r"https://xz.aliyun.com"+''.join(i.xpath(r'//p[@class="topic-summary"]/a/@href')).strip()
				date = "[【" + str(comments) + "】  /" + title +"](" + href +")  \r"			#写成markdown中的链接格式
				print(date)
				list.append(date)
			time.sleep(2)
	except Exception as e:
		write_md()
		raise e 

main()

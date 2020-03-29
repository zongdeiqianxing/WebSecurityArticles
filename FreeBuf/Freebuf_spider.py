#coding:utf-8
import requests,time
from lxml import etree

base_url=r"https://www.freebuf.com/articles/web/page/"				#可以替换web为其他tags
list20,list50,list70=[],[],[]
headers = {
    'User-Agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13',
}

def write_md():
	date = time.strftime("%Y%m%d", time.localtime())
	for i in ["20w","50w","70w"]:
		filename=i + "+FreebufArticles-" + date + '.md'
		with open(filename,'a+') as f:
			if i == "20w":
				for line in list20:
					f.write(line)
			if i == "50w":
				for line in list50:
					f.write(line)
			if i == "70w":
				for line in list70:
					f.write(line)
					
def main():	
	try:
		for n in range(1,1000):
			url=base_url+str(n)
			print("正在读取："+url)
			result = requests.get(url=url,headers=headers).text
			#print(result)
			if 'page404' in result:
				write_md()
				exit("已爬完-_-")

			tree = etree.HTML(result)
			xpath=tree.xpath(r'//*[@id="timeline"]/div')
			if xpath is None:
				write_md()
				exit("出错-_-")
				
				
			for i in xpath:
				i=etree.HTML(etree.tostring(i).decode('utf-8'))
				readNum=''.join(i.xpath(r'//div[@class="news_bot"]/span[2]/strong[1]/text()'))
				if int(readNum) < 200000:
					continue
				readNum=int(readNum[:-4])
				title=''.join(i.xpath(r'//div[@class="news-info"]/dl/dt/a/text()'))
				href=''.join(i.xpath(r'//div[@class="news-info"]/dl/dt/a/@href'))
				date = "[【" + str(readNum) + "w】  /" + title +"](" + href +")  \r\n"			#写成markdown中的链接格式
				print(date)
				if 20 <= readNum < 50:
					list20.append(date)
				if 50 <= readNum < 70:
					list50.append(date)
				if 70 <= readNum:
					list70.append(date)
			time.sleep(2)
	except Exception as e:
		write_md()
		raise e 
	

main()
	
	
	
	
	
	
	

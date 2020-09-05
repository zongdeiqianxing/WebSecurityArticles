#coding:utf-8
import requests,time
from lxml import etree

base_url=r"https://www.leavesongs.com/list/?page="				
list=[]
headers = {
    'User-Agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13',
}

def write_md():
	date = time.strftime("%Y%m%d", time.localtime())
	filename="leavesongs-all-" + date + '.md'
	with open(filename,'w+') as f:
		for line in list:
			f.write(line)
			
def getReadNum(url):
	result = requests.get(url=url,headers=headers).text
	tree = etree.HTML(result)
	ReadNums=''.join(tree.xpath(r'/html/body/div[2]/article/header/div/div[2]/text()')).strip()
	#print(ReadNums[3:])
	return ReadNums[3:]
	
def main():	
	pages = 1 
	try:
		for n in range(1,1000):
			url=base_url+str(n)
			print("正在读取："+url)
			result = requests.get(url=url,headers=headers).text
			#print(result)
				
			tree = etree.HTML(result)
			if pages == 1 :
				pages=int(''.join(tree.xpath(r'/html/body/div/nav/ul/li[9]/a/text()')))	#获取最大页
			elif pages != 1 and pages < n:
				write_md()
				exit("已经爬完；")
				
			xpath=tree.xpath(r'/html/body/div/ul/li')
			if xpath is None:
				write_md()
				exit("出错-_-")
			
			for i in xpath:
				i=etree.HTML(etree.tostring(i).decode('utf-8'))
				title =''.join(i.xpath(r'//span/a/text()')).strip()
				#print(title)
				href=r"https://www.leavesongs.com"+''.join(i.xpath(r'//span/a/@href')).strip()
				time.sleep(5)
				ReadNums=getReadNum(href)
				if ReadNums is not None:
					ReadNums=ReadNums[:-3]
				date = "[【" + ReadNums + "k】  /" + title +"](" + href +")  \r"			#写成markdown中的链接格式
				#date = "[" + title +"](" + href +")  \r"
				print(date)
				list.append(date)
			time.sleep(5)
	except Exception as e:
		write_md()
		raise e 

main()

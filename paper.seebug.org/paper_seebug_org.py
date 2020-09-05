#coding:utf-8
import requests,time
from lxml import etree

#base_url=r"https://paper.seebug.org/category/web-security/?page="			
data=[]
headers = {
	'User-Agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13',
}

def write_md(category):
	date = time.strftime("%Y%m%d", time.localtime())
	filename=category + "-" + date + '.md'
	with open(filename,'a+',errors='ignore') as f:
		for line in data:
			f.write(line)

def main(category):	
	number=1
	try:
		for page in range(1,1000):
			url=r'https://paper.seebug.org/category/{}/?page={}'.format(category,str(page))
			print("reading：" + url)
			result = requests.get(url=url,headers=headers).text
			#print(result)
			if '没有搜到Paper' in result:
				write_md(category)
				break

			tree = etree.HTML(result)
			#//*[@id="wrapper"]/main/div/article[1]/header/h5/a
			xpath=tree.xpath(r'//*[@id="wrapper"]/main/div/article')
			print(xpath)
			if xpath is None:
				write_md()
				exit("error-_-")
				
			
			for i in xpath:
				i=etree.HTML(etree.tostring(i).decode('utf-8'))
				title =''.join(i.xpath(r'//header/h5/a/text()')).strip()
				print(title)

				href=r"https://paper.seebug.org"+''.join(i.xpath(r'//header/h5/a/@href')).strip()
				row = "[" + str(number) + "	 /" + title +"](" + href +")  \r"			
				number += 1
				print(row)
				data.append(row)
			time.sleep(1)
	except Exception as e:
		write_md(category)
		raise e 

categories=["web-security","tools","experience","vul-analysis","mobile-security","ctf","404team",]	
for category in categories:
	main(category)
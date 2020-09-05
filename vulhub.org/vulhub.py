#d此脚本不是爬虫，需要下载https://github.com/vulhub/vulhub到w本地，在本地文件夹下使用脚本
import os

base_dir= 'vulhub'
base_url=r'https://github.com/vulhub/vulhub/blob/master/'
files_README = []


def getTitle(file):
	with open(file,'r') as f:
		Title = f.readline()
		if '# ' not in Title:
			print("file not found Titie:",file)
		return Title
	
#本来想用title重新copy并命名文件的，但是考虑到图片会不显示 不做了
#def copyREADME(file,title):
#	if not os.path.exists('vulhub-README'):
#		os.mkdir('vulhub-README')
#	command = "cp " + file + ' ' + r"vulhub-README/" + r" "
#	os.system()

for root, dirs, files in os.walk(base_dir,topdown=False):
	for name in files:
		if 'README.md' in name:
			README_zh = os.path.join(root,'README.zh-cn.md')
			if os.path.exists(README_zh):
				#print(README_zh)
				files_README.append(README_zh)
			else:
				#print(os.path.join(root, name))
				files_README.append(os.path.join(root, name))


with open('vulhubTitle.md','w+') as f:
	for file in files_README:
		Title = getTitle(file)
		if file.split('/',1)[0] == 'vulhub':
			path = file.split('/',1)[1]
		content = '[' + Title.strip() + '](' + base_url + path + ')  \r'
		f.write(content)

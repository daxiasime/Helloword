# downloader.py

import re
import requests
import queue
import threading
import os
import time
from urllib import parse

def geturl(url1,url2):
	u1_list=url1.split('/')[:-1]
	u2_list=url2.split('/')
	ls=u1_list+u2_list
	url_ls=list(set(ls))
	url_ls.sort(key=ls.index)
	url='/'.join(url_ls)
	print(url)
	return url

def request(url):
	res=requests.get(url)
	if res.status_code == requests.codes.ok:
		return res
	else :
		print("z网络状态不好！")
		while res.status_code == requests.codes.ok:
			time.sleep(3)
			print("正在尝试！\r",end="")
			res=requests.get(url)
		return res

def add_equeue(url):
	s=request(url).text
	m3u8_p=re.compile("\n?#EXTM3U\n?#EXT-X-STREAM-INF",re.M)
	ts_p=re.compile("\n?#EXTM3U\n?#EXT-X-VERSION",re.M)
	if re.match(m3u8_p,s)!=None and 'm3u8'in s:
		print("this is m3u8 file")
		print("正在获取 m3u8 file")
		m3u8_h=s.strip().split('\n')[-1]
		url=geturl(url,m3u8_h)
		s=request(url).text
	if re.match(ts_p,s)!=None and 'ts'in s:
		print("this is ts file")
		ts_d=s.split('\n')[3::2][1:-1]
		# print(ts_d)
		ts_data = queue.Queue(len(ts_d))
		print(f"添加到队列{len(ts_d)}")
		for it in ts_d:
			url=geturl(url,it)
			x={'url':url,'name':it.replace('/','_')}
			ts_data.put(x)
			
		print(f"添加到队列,共计{ts_data.qsize()}")
		return ts_data
	else: 
		print("数据异常！")
		return None
def process_bar(current,total):
	index=round((1-current/total)*100,1)
	s1=' '*round((100-index)/2)
	s2='▊'*round(index/2)
	print(f"|{s2+s1}|{index}%\r",end="")





class download_m3u8(threading.Thread):
	def __init__(self, threadID,q):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.q = q
	def run(self):
		# print ("开启线程：" + self.name)
		self.__download_ts(self.threadID,self.q)
		# print ("退出线程：" + self.name)

	def __download_ts(self,threadID,q):
		while not (q.empty() and finsh_download):	
			it=q.get()
			url=it['url']
			name=it['name']
			if os.path.exists(_PATH+name):
				print("已下载")
			else:
				data=request(url).content
				print(f"下载{name} ")
				print(f"下载{url} ")
				with open(_PATH+name,'wb') as f:
					f.write(data)
			if os.path.exists(_PATH+name):
				# 下载成功
				q.task_done()
			else:
				print(f"{it['name']}下载失败，已放入队列。")
				q.put(it)
			if q.empty() :
				finsh_download=True

def get_address(url):
	html=request(url).text
	pattern = re.compile('http.*?.m3u8',re.M)
	p = re.compile('<title>(.*?)</title>',re.M)
	name=re.findall(p,html)[0].replace('<','_')
	name=name.replace('>','_')
	result=re.findall(pattern,html)[0]
	result = parse.unquote(result)
	print(name,result)
	return name,result

# url="http://meng.wuyou-zuida.com/20200404/28799_829a960d/index.m3u8"


def main_(url):

	_PATH="./m3u8downloader"
	_THREAD_COUNT=5
	if not os.path.exists(_PATH):
		os.mkdir(_PATH)
	name,url=get_address(url)
	_PATH=_PATH+'/'+name
	if not os.path.exists(_PATH):
		os.mkdir(_PATH)
	_PATH=_PATH+'/'

	finsh_download=False
	threads=[]
	ts_data=add_equeue(url)
	size=ts_data.qsize()
	if ts_data!=None:
		for threadID in [i for i in range(_THREAD_COUNT)]:
			thread = download_m3u8(threadID, ts_data)
			thread.start()
			threads.append(thread)
		# 等待队列清空
		while not ts_data.empty():
			time.sleep(0.2)
			process_bar(ts_data.qsize(),size)
		# 等待所有线程完成

		for t in threads:
			t.join()
		os.chdir(_PATH)
		print(f"cat *.ts >> {name}.mp4")
		os.system(f"cat *.ts >> {name}.mp4")

		if os.path.exists(f"{name}.mp4"):
			os.system(f"rm -r *.ts")
		else:
			print("合并出错！")
		print ("\n退出主线程")

	else:
		print('erro')

_PATH="./m3u8downloader"
_THREAD_COUNT=5
for page in range(5,10):
	url=f"https://www.diediaow.com/play/17815-0-{page}.html"
	main_(url)
	time.sleep(3)

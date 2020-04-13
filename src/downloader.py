# downloader.py

import re
import requests
import queue
import threading
url="http://meng.wuyou-zuida.com/20200404/28799_829a960d/index.m3u8"
url_head="http://meng.wuyou-zuida.com/20200404/28799_829a960d/"

def add_equeue(url):
	res=requests.get(url)
	if res.status_code == requests.codes.ok:
		s=res.text
	else :
		print("z网络状态不好！")
		while True:
			time.sleep(3)
			print("正在尝试！\r",end="")

	m3u8_p=re.compile("\n?#EXTM3U\n?#EXT-X-STREAM-INF",re.M)
	ts_p=re.compile("\n?#EXTM3U\n?#EXT-X-VERSION",re.M)
	if re.match(m3u8_p,s)!=None and 'm3u8'in s:
		print("this is m3u8 file")
		print("正在获取 m3u8 file")
		s=requests.get(url_head+s.strip().split('\n')[-1]).text
	if re.match(ts_p,s)!=None and 'ts'in s:
		print("this is ts file")
		ts_d=s.split('\n')[3::2][1:-1]
		# print(ts_d)
		ts_data = queue.Queue(len(ts_d))
		print(f"添加到队列{len(ts_d)}")
		for it in ts_d:
			x={'url':url_head+it,'name':it}
			ts_data.put(x)
			

		print(f"添加到队列,共计{ts_data.qsize()}")
		return ts_data
	else: 
		print("数据异常！")
		return None
class download_m3u8(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
    def run(self):
        # print ("开启线程：" + self.name)
        self.__download_ts(self.threadID,self.q)
        # print ("退出线程：" + self.name)

    def __download_ts(self,threadID,q):
    	it=q.get()
    	url=it['url']
    	name=it['name']
    	data=requests.get(url).content
    	with open(path+name,'wb') as f:
	    	f.write(data) 

path="../res/ts/"
add_equeue(url)

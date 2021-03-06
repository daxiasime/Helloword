# word_sagmentation.py
import pandas
import numpy
import re
import math,time
class word_sagment(object):
	def __init__(self,max_step=5,offset=3000):
		self.max_step=max_step
		self.dic=self.load_ciku_2()
		self.offset=offset
		self.time=""
	def add(self,word):
		self.dic[word]=100000
	def cut(self ,text):
		self.time = time.clock()
		p=re.compile("[a-z，\-。\"、·：,【】|、\d — “!@$^&*”！#%……&×（）  \n \t \b～]",re.M)
		lis_sen=[ x for x in re.split(p,text) if x!=""]
		# print('拆分句子完成...')
		# 将段落拆分为单个句子
		words=[]
		# print(lis_sen)
		import queue
		sentence_que=queue.Queue(len(lis_sen))
		for x in lis_sen:
			sentence_que.put(x)
		while not sentence_que.empty():
			sentence=sentence_que.get()
			wordlist_= self.segmentation(sentence)
			if wordlist_==None:
				sentence_que.put(sentence)
			else:
				sentence_que.task_done()
				for word  in wordlist_:
					words.append(word)
		return words


	def devide(self,s):
		a=[]
		for j in range(1,self.max_step+1):
			c=[]
			for i in range(len(s)):
				c.append(s[i:i+j])
			a=a+c
		# print(a)
		return a
	def load_ciku_2(self):
		data=pandas.read_csv("res/CorpusWordlist.csv",sep='\t')
		data_=numpy.array(data)
		# print("加载词库....")
		dic=[x[0].split(',')[1::2] for x in data_[0:]]
		# print(dic[:3])
		dic={x[0]:-math.log(eval(x[1])/100) for x in dic}
		# print("解析完成..")
		return dic

	def load_ciku(self):
		data=pandas.read_csv("../res/dict_.csv",sep='\t')
		data_=numpy.array(data)
		# print("加载词库....")
		dic=[x[0].split(',') for x in data_]
		# print("解析词库....")
		dic={x[0]:x[1].split(' ')[0] for x in dic}
		# print("解析完成..")
		return dic

	def dict_filter(self,sentence):
		res=self.devide(sentence)
		dic=self.dic
		dictory={}
		for x in res:
			if dic.__contains__(x):
				dictory[x]=int(dic[x])
				if len(x)==1:
					dictory[x]*=self.offset#消除单字过分的影响。
		# print(dictory)
		return dictory


	def get_min_cost(self,cost,best):
		min_,path=1000,0
		for x in cost:
			if best[x[0]-1]+int(x[1]) < min_:
				# print(int(x[1]))
				min_=best[x[0]-1]+x[1]
				path=x[0]-1
		return min_,path
	def creat_words_graph(self,sentence,dictory):
# 		dictory={"经常":0.23, "经":0.3, "有":0.23, "有意见":0.23,"意见":0.16,
# "分歧":0.16,"见":0.3,"意":0.3,"见分歧":0.3, "分":0.23,"我":0.16}
		length=len(sentence)

		words_graph={x+1 : [] for x in range(length+1)}
		for i in range(2,length+2):
			distance=1000
			if dictory.__contains__(sentence[i-2]):
				distance=dictory[ sentence[i-2] ]
			words_graph[i].append( [i-1, distance ]  )
		dict_=[list(x) for x in list(dictory.items())]
		for x in dict_:
			if len(x[0])==1:
				continue
			start=0
			while sentence.index( x[0][-1],start)+2< sentence.index(x[0][0]) +1:
				#由重复关键字造成的异常.使用 start去掉不合法的部分
				start=sentence.index( x[0][-1],start)+1
			words_graph[sentence.index( x[0][-1],start)+2].append([sentence.index(x[0][0]) +1, x[1] ])
		# print(words_graph)
		return words_graph

	def get_shorts_path(self,sentence,words_graph):
		length=len(sentence)
		best=[0 for x in range(length+1)]
		path=[0 for x in range(length+1)]
		path[0]=-1
		for i in range(1,length+1):
			best[i],path[i]=self.get_min_cost(words_graph[i+1],best)
		path=[i+1 for i in path ]
		short_path=[]
		# print(best)
		print(path)
		print(sentence)
		i=length
		short_path.append(i+1)
		count=0
		while path[i] !=0 and count<length+5:
			count+=1
			node=path[i]
			short_path.append(node)
			i=node-1
		if path[i]==0:
			short_path.reverse()
			return short_path
		else:
			print("正在重试")
			return None

	def segmentation(self,sentence):
		dictory=self.dict_filter(sentence)
		# print('过滤字典完成')
		words_graph=self.creat_words_graph(sentence,dictory)
		# print('创建词组图完成...')

		short_path=self.get_shorts_path(sentence,words_graph)
		if short_path==None:
			return None
		#将路径转化为单词
		# print("计算最短路径成功.....")
		l=len(short_path)
		word=[]
		for x in range(l-1):
			word.append(sentence[short_path[x]-1:short_path[x+1]-1])
		print(f"转化词组完成....用时:{round(time.clock()-self.time,3)}s")
		return word



# word_sa=word_sagment(offset=1)
# text='''
# 没有告诉婆娘任何人
# '''
# words=word_sa.cut(text)
# print()
# print(words)
# test.py
import re
import collections
from collections import Counter
import jieba,json
import pandas as pd
import numpy
from  math import log

# p=re.compile('class="content">\n(.*? *  )</div>',re.S)
# print(re.findall(p,text))

def copy_word(sentence):
	#分词,过滤 返回列表.
	stop_word = open('NLP/corpurs/stop_word.txt').read().split('\n')
	p=re.compile('[^(\\u4e00-\\u9fa5)]',re.S)
	sentence=re.sub(p,' ',sentence)
	sentence = ' '.join(sentence.split())#将多个空格合并为一个
	# print(sentence)
	res=list(jieba.cut(sentence))
	global c
	global k
	c+=1
	# 分批次处理
	if c%1000==0:
		k+=1
	with open(f"/home/devin/baidunetdiskdownload/tieba.sag{k}",'a') as f:
		f.write(" ".join(res)+"\n")

	return res 


def calculate_frequence(words):
	with open("NLP/corpurs/length",'r') as f:
		length=int(f.read())
	length+=len(words)
	frequency_uni=Counter(words)
	df = pd.read_csv('NLP/corpurs/unigram.csv')
	frequency_uni_old=dict(zip(list(df.words),list(df.Z_count)))
	# print(frequency_uni_old)
	for key in frequency_uni:
		if frequency_uni_old.get(key):
			frequency_uni_old[key]=frequency_uni_old[key]+frequency_uni[key]
		else:
			frequency_uni_old[key]=frequency_uni[key]
	# for i in list(frequency_uni_old):
	# 	if frequency_uni_old.get(i)<5:
	# 		del frequency_uni_old[i]
	with open('NLP/corpurs/length' ,'w') as f:
		f.write(str(length))

	# print(frequency_uni_old)
	if len(frequency_uni_old)==0:
		return -1
	dataframe = pd.DataFrame({'_count':list(frequency_uni_old.values()),'words':list(frequency_uni_old.keys())})
	#将DataFrame存储为csv,index表示是否显示行名，default=True
	dataframe.to_csv("NLP/corpurs/unigram.csv",index=False,sep=',')
	return 1

def remove():
	with open("NLP/corpurs/length",'r') as f:
		length=int(f.read())

	df = pd.read_csv('NLP/corpurs/unigram.csv')
	frequency_uni_old=dict(zip(list(df.words),list(df._count)))
	for i in list(frequency_uni_old):
		if frequency_uni_old.get(i)<5:
			del frequency_uni_old[i]

	dataframe = pd.DataFrame({'_count':list(frequency_uni_old.values()),'words':list(frequency_uni_old.keys())})
	#将DataFrame存储为csv,index表示是否显示行名，default=True
	dataframe.to_csv("NLP/corpurs/unigram.csv",index=False,sep=',')

def get_p(word):
	df = pd.read_csv('NLP/corpurs/unigram.csv')
	frequency_uni_old=dict(zip(list(df.words),list(df._count)))
	with open("NLP/corpurs/length",'r') as f:
		length=int(f.read())
	k=1
	return (frequency_uni_old.get(word)+k)/(length+k*length)

def change_bi_words(words):
	print("读取结束")
	bi_words=[]
	tri_words=[]
	for x in range(len(words)-2):
		bi_words.append(words[x]+words[x+1])
		tri_words.append(words[x]+words[x+1]+words[x+2])
	bi_words.append(words[-2]+words[-1])
	frequency_bi=Counter(bi_words)
	frequency_tri=Counter(tri_words)

	df_bi = pd.read_csv('NLP/corpurs/bigram.csv')
	df_tri = pd.read_csv('NLP/corpurs/trigram.csv')

	frequency_bi_old=dict(zip(list(df_bi.words),list(df_bi._count)))
	# print(frequency_uni_old)
	for key in frequency_bi:
		if frequency_bi_old.get(key):
			frequency_bi_old[key]=frequency_bi_old[key]+frequency_bi[key]
		else:
			frequency_bi_old[key]=frequency_bi[key]

	# print(frequency_bi_old)
	dataframe = pd.DataFrame({'_count':list(frequency_bi_old.values()),'words':list(frequency_bi_old.keys())})
	#将DataFrame存储为csv,index表示是否显示行名，default=True
	dataframe.to_csv("NLP/corpurs/bigram.csv",index=False,sep=',')

	frequency_tri_old=dict(zip(list(df_tri.words),list(df_tri._count)))
	# print(frequency_uni_old)
	for key in frequency_tri:
		if frequency_tri_old.get(key):
			frequency_tri_old[key]=frequency_tri_old[key]+frequency_tri[key]
		else:
			frequency_tri_old[key]=frequency_tri[key]

	# print(frequency_tri_old)
	dataframe = pd.DataFrame({'_count':list(frequency_tri_old.values()),'words':list(frequency_tri_old.keys())})
	#将DataFrame存储为csv,index表示是否显示行名，default=True
	dataframe.to_csv("NLP/corpurs/trigram.csv",index=False,sep=',')

class LM(object):
	"""docstring for LM"""
	def __init__(self):
		super(LM, self).__init__()
		df_uni = pd.read_csv('NLP/corpurs/unigram.csv')
		df_bi = pd.read_csv('NLP/corpurs/bigram.csv')
		df_tri = pd.read_csv('NLP/corpurs/trigram.csv')
		self.stop_word=open('NLP/corpurs/stop_word.txt').read().split('\n')
		self.length=int(open('NLP/corpurs/length').read())
		self.k=2
		self.stop_word.append('\n')
		self.frequency_uni=dict(zip(list(df_uni.words),list(df_uni._count)))
		self.frequency_bi=dict(zip(list(df_bi.words),list(df_bi._count)))
		self.frequency_tri=dict(zip(list(df_tri.words),list(df_tri._count)))
		

	def sqlit_word(self,sentence):
		#分词,过滤 返回列表.
		for i in self.stop_word:
			sentence=sentence.replace(i,'')
		res=list(jieba.cut(sentence))
		return res 

	def frequency(self,word):
		if self.frequency_uni.__contains__(word):
			return (self.frequency_uni[word]+self.k)/(self.length*self.k)
		else:
			return self.k/(self.length*self.k)

	def calculate_condition_probability(self,word_a,word_b):
		# print(word_a,word_b)
		count,count_w=0,0
		# print(data_length)
		if self.frequency_uni.__contains__(word_b):
			count+=self.frequency_uni[word_b]
		if self.frequency_bi.__contains__(word_a+word_b):
			count_w+=self.frequency_bi[word_a+word_b]
		return (count_w+self.k)/(count+self.length*self.k)

	def calculate_condition_probability_3(self,word_a,word_b,word_c):
		# print(word_a,word_b)
		count,count_w=0,0
		if self.frequency_bi.__contains__(word_b+word_c):
			count+=self.frequency_bi[word_b+word_c]
		if self.frequency_tri.__contains__(word_a+word_b+word_c):
			count_w+=self.frequency_tri[word_a+word_b+word_c]
		return (count_w+self.k)/(count+self.length*self.k)

	def unigram(self,sentence):
		words=self.sqlit_word(sentence)
		# print(words)
		p=self.frequency(words[0])
		for x in range(0,len(words)):
			p*=self.frequency(words[x])
		return p

	def bigram(self,sentence):
		words=self.sqlit_word(sentence)
		# print(words)
		p=self.frequency(words[0])
		for x in range(len(words)-1):
			p*=self.calculate_condition_probability(words[x+1],words[x])
		return p

	def trigram(self,sentence):
		words=self.sqlit_word(sentence)
		# print(words)
		if len(words)<3:
			print(words)
			print("长度不足")
			return -1
		p=self.frequency(words[0])
		p*=self.calculate_condition_probability(words[1],words[0])
		for x in range(len(words)-2):
			p*=self.calculate_condition_probability_3(words[x+2],words[x+1],words[x])
		return p

	def get_perplexity(self,sentence):
		words=self.sqlit_word(sentence)
		# print(words)
		p=log(self.frequency(words[0]))
		for x in range(len(words)-1):
			p+=log(self.calculate_condition_probability(words[x+1],words[x]))
		p=2**(-(p)/len(words))
		return p

	def study(self,URL):	
		c=0
		k=0
		words=""
		count=0
		all_=1120000
		with open('/home/devin/baidunetdiskdownload/tieba.dialogues','r') as f:
			for s in f:
				count+=1
				words+=" "+s
				if count%150==0:
					calculate_frequence(copy_word(words))
					words=""
					print(f'已经学习: {count/all_}')

		for i in range(10):
			with open('/home/devin/baidunetdiskdownload/tieba.sag0','r') as f:
				words=f.read().split(' ')
			change_bi_words(words)
			print("完成一个")

lm=LM()
if lm.bigram("今天天气好,我想去运动")>lm.bigram("我开心很干嘛在你"):
	print("s1是人话")
	print(lm.get_perplexity("今天天气好,我想去运动"))
else:
	print(lm.get_perplexity("今天天气好,我想去运动"))
	print("s2是人话")

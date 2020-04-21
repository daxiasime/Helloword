# word_representation.py
import numpy
import math
import word_sagmentation as ws
from numpy import mat,dot
from math import sqrt
#余弦相似度
sentence1="我们今天又去运动"
sentence2="你们昨天又去跑步"
sentence3="你们昨天又去跑步,又去运动"

sen_lib=["我们今天又去运动","你们昨天又去跑步","你们昨天又去跑步,又去运动"]
a=""
ws_c=ws.word_sagment(offset=20)
with open('res/text.txt','r') as f:
	a=f.read()
dictionary=ws_c.cut("我们今天又去运动,你们昨天跑步")

# ['我们', '今天', '又', '去', '运动', '你们', '昨天', '跑步']
# one-hot representation
def  get_one_hot(sentence):
	s1_list=ws_c.cut(sentence)
	one_hot_s1=[]
	for x in dictionary:
		if  x in s1_list:
			one_hot_s1.append(1)
			continue
		one_hot_s1.append(0)
	return one_hot_s1
	#count-base-representation
def  get_count_base(sentence):
	s1_list=ws_c.cut(sentence)
	one_hot_s1=[]
	for x in dictionary:
		if  x in s1_list:
			one_hot_s1.append(s1_list.count(x))
			continue
		one_hot_s1.append(0)
	return one_hot_s1

# TF-idf
def get_idf(x):
	count=0
	for sentence in sen_lib:
		if x in sentence:
			count+=1
	return math.log(len(sen_lib)/count)

def  tf_idf(sentence):
	s1_list=ws_c.cut(sentence)
	one_hot_s1=[]
	for x in dictionary:
		if  x in s1_list:
			ele=s1_list.count(x)*get_idf(x)
			one_hot_s1.append(ele)
			continue
		one_hot_s1.append(0)
	return one_hot_s1




def cosin_similarity(a,b):return numpy.dot(a,b)/math.sqrt(numpy.dot(a,a)*numpy.dot(b,b))

def calculate_distance(a,b):
	for  x in range(len(a)):
		a[x]-=b[x]
	return sqrt(dot(a,a))
# print(calculate_distance(get_one_hot(sentence1),get_one_hot(sentence2)))
# print(calculate_distance(get_one_hot(sentence1),get_one_hot(sentence3)))
# print(calculate_distance(get_one_hot(sentence2),get_one_hot(sentence3)))
# print(cosin_similarity(get_one_hot(sentence1),get_one_hot(sentence2)))
# print(cosin_similarity(get_one_hot(sentence1),get_one_hot(sentence3)))
# print(cosin_similarity(get_one_hot(sentence2),get_one_hot(sentence3)))
# print("---"*20)
# print(calculate_distance(get_count_base(sentence1),get_count_base(sentence2)))
# print(calculate_distance(get_count_base(sentence1),get_count_base(sentence3)))
# print(calculate_distance(get_count_base(sentence2),get_count_base(sentence3)))
# print(cosin_similarity(get_count_base(sentence1),get_count_base(sentence2)))
# print(cosin_similarity(get_count_base(sentence1),get_count_base(sentence3)))
# print(cosin_similarity(get_count_base(sentence2),get_count_base(sentence3)))
# print("---"*20)
# print(calculate_distance(tf_idf(sentence1),tf_idf(sentence2)))
# print(calculate_distance(tf_idf(sentence1),tf_idf(sentence3)))
# print(calculate_distance(tf_idf(sentence2),tf_idf(sentence3)))
# print(cosin_similarity(tf_idf(sentence1),tf_idf(sentence2)))
# print(cosin_similarity(tf_idf(sentence1),tf_idf(sentence3)))
# print(cosin_similarity(tf_idf(sentence2),tf_idf(sentence3)))
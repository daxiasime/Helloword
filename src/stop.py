# import jieba
# jieba.add_word("奥利给")
# print(jieba.lcut("经常有意见分歧 我是一个小可爱，加油奥利给"))
import pandas
import numpy
import json
s="人们在一家超市外保持间距排队等待购物"
def devide(s,max_step=4):
	a=[]
	for j in range(1,max_step+1):
		c=[]
		for i in range(len(s)):
			c.append(s[i:i+j])
		a=a+c
	return list(set(a))
res=devide(s,max_step=5)

data=pandas.read_csv("../res/dict_.csv",sep='\t')
data_=numpy.array(data)
dic=[x[0].split(',') for x in data_]
dic={x[0]:x[1].split(' ')[0] for x in dic}
cost={}
for x in res:
	cost[x]=100000
	if dic.__contains__(x):
		cost[x]=1/int(dic[x])
print(cost)


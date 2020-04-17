# word_sagmentation.py
import pandas
import numpy
import json
def devide(s,max_step=4):
	a=[]
	for j in range(1,max_step+1):
		c=[]
		for i in range(len(s)):
			c.append(s[i:i+j])
		a=a+c
	return list(set(a))

def get_dict(s,max_step=5):
	res=devide(s,max_step=5)
	data=pandas.read_csv("../res/dict_.csv",sep='\t')
	data_=numpy.array(data)
	dic=[x[0].split(',') for x in data_]
	dic={x[0]:x[1].split(' ')[0] for x in dic}
	d={}
	for x in res:
		d[x]=1000
		if dic.__contains__(x):
			d[x]=1/int(dic[x])
			if len(x)==1:
				d[x]*=2000#消除单字过分的影响。

	return d


def get_min_cost(cost,best):
	min_,path=1000,0
	for x in cost:
		if best[x[0]-1]+int(x[1]) < min_:
			min_=best[x[0]-1]+int(x[1])
			path=x[0]-1
	return min_,path



def segmentation(sentence,max_step=5):
	dictory=get_dict(sentence,max_step=5)
	# dictory={"经常":2.3, "经":3, "有":2.3, "有意见":2.3,"意见":1.6,"分歧":1.6,"见":3,"意":3,"见分歧":3, "分":2.3,"我":1.6}
	length=len(sentence)
	best=[0 for x in range(length+1)]
	path=[0 for x in range(length+1)]
	path[0]=-1
	cost={x+1 : [] for x in range(length+1)}
	# "  经    常    有    意    见    分   歧"
	#  1    2     3     4    5     6    7     8
	# init cost
	for i in range(2,length+2):
		distance=200
		if dictory.__contains__(sentence[i-2]):
			distance=dictory[ sentence[i-2] ]
		cost[i].append( [i-1, distance ]  )

	dict_=[list(x) for x in list(dictory.items())]
	# print(dict_)
	for x in dict_:
		if len(x[0])==1:
			continue
		# print(x[0][-1],x[0][0])
		# print(sentence.index( x[0][-1])+1,[sentence.index(x[0][0]) +1, x[1] ])
		cost[sentence.index( x[0][-1])+2].append([sentence.index(x[0][0]) +1, x[1] ])
	print(cost)


	for i in range(1,length+1):
		best[i],path[i]=get_min_cost(cost[i+1],best)
		# print(best[i],path[i])
	path=[i+1 for i in path ]
	print(best)
	# print('ssss')
	# print(path)
	short_path=[]
	i=length
	short_path.append(i+1)

	while path[i] !=0:
		node=path[i]
		short_path.append(node)
		i=node-1
	short_path.reverse()
	print(f"花费：{best[length]}\n路径： {short_path}\n")
	l=len(short_path)
	word=[]
	for x in range(l-1):
		word.append(sentence[short_path[x]-1:short_path[x+1]-1])
	print(word)
	return word






sentence="我们经常有意见分歧"
s="函数调用使用关键字参数来确定传入的参数值"

segmentation(sentence)
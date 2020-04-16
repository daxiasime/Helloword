# word_sagmentation.py

def get_min_cost(cost,best):
	min_,path=1000,0
	for x in cost:
		if best[x[0]-1]+x[1] < min_:

			min_=best[x[0]-1]+x[1]
			path=x[0]-1
	return round(min_,1),path



def segmentation(sentence,dictory):

	best=[0 for x in range(len(sentence)+1)]
	path=[0 for x in range(len(sentence)+1)]
	path[0]=-1

	cost={x+1 : [] for x in range(len(sentence)+1)}
	# "  经    常    有    意    见    分   歧"
	#  1    2     3     4    5     6    7     8
	# init cost
	for i in range(2,9):
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
	# print(cost)


	for i in range(1,8):
		best[i],path[i]=get_min_cost(cost[i+1],best)

		# print(best[i],path[i])



	path=[i+1 for i in path ]
	# print(best)
	# print('ssss')
	# print(path)

	short_path=[]
	i=7
	short_path.append(8)

	while path[i] !=0:
		node=path[i]
		short_path.append(node)
		i=node-1
	short_path.reverse()
	print(f"花费：{best[7]}\n路径： {short_path}\n")
	l=len(short_path)
	word=[]

	for x in range(l-1):
		word.append(sentence[short_path[x]-1:short_path[x+1]-1])
	print(word)
	return word


dictory={
  "经常":2.3,
  "经":3,
  "有":2.3,
  "有意见":2.3,
  "意见":1.6,
  "分歧":1.6,
  "见":3,
  "意":3,
  "见分歧":3,
  "分":2.3,
}

sentence="经常有意见分歧"
segmentation(sentence,dictory)
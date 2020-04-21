# language_mode.py

from collections import Counter
import jieba
import re,json 

from math import log 
def words_func(text): return list(jieba.cut(text))
def change_bi_words(words):
	print("读取结束")
	bi_words=[]
	for x in range(len(words)-1):
		bi_words.append(words[x]+words[x+1])
	return bi_words
def change_tri_words(words):
	print("读取结束")
	tri_words=[]
	for x in range(len(words)-2):
		tri_words.append(words[x]+words[x+1]+words[x+2])
	return tri_words
def calculate_frequence(words):
	bi_words=change_bi_words(words)
	tri_words=change_tri_words(words)
	stop_word = open('corpurs/stop_word.txt').read().split('\n')
	frequency_uni=Counter(words)
	frequency_bi=Counter(bi_words)
	frequency_tri=Counter(tri_words)
	data={
		"data_length":len(words),
		"frequency_uni":frequency_uni,
		"frequency_bi":frequency_bi,
		"frequency_tri":frequency_tri
	}
	js_data=json.dumps(data,ensure_ascii=False)
	with open('corpurs/jsdata.json','w') as f:
		f.write(js_data)
	print('计算频率成功')
def init():
	with open('corpurs/text.txt','r') as f:
		WORDS=f.read()
	stop_word = open('corpurs/stop_word.txt').read().split('\n')
	WORDS=" ".join(words_func(WORDS))
	stop_word.append('\n')
	for i in stop_word:
		WORDS=WORDS.replace(i,' ')
	words=re.sub(' * ', '/', WORDS)
	with open('corpurs/text_seg.txt','w') as f:
		f.write(words)	
	print("分词写入成功")
	with open('corpurs/text_seg.txt','r') as f:
		words=f.read()
	calculate_frequence(words.split('/'))

def get_frequency_list():
	with open('corpurs/jsdata.json','r') as f:
		words=f.read()
	frequency_list=json.loads(words)
	print("读取结束")
	return frequency_list['data_length'],frequency_list['frequency_uni'],frequency_list['frequency_bi'],frequency_list['frequency_tri']

data_length,frequency_uni,frequency_bi,frequency_tri=get_frequency_list()

def copy_word(sentence):
	#分词,过滤 返回列表.
	stop_word = open('corpurs/stop_word.txt').read().split('\n')
	for i in stop_word:
		sentence=sentence.replace(i,'')
	res=list(jieba.cut(sentence))
	return res 

def frequency(word):
	if frequency_uni.__contains__(word):
		return (frequency_uni[word]+1)/(data_length*1)
	else:
		return 1/(data_length*1)

def calculate_condition_probability(word_a,word_b):
	# print(word_a,word_b)
	count,count_w=0,0
	# print(data_length)
	if frequency_uni.__contains__(word_b):
		count+=frequency_uni[word_b]
	if frequency_bi.__contains__(word_a+word_b):
		count_w+=frequency_bi[word_a+word_b]
	return (count_w+1)/(count+data_length)

def calculate_condition_probability_3(word_a,word_b,word_c):
	# print(word_a,word_b)
	count,count_w=0,0
	if frequency_bi.__contains__(word_b+word_c):
		count+=frequency_bi[word_b+word_c]
	if frequency_tri.__contains__(word_a+word_b+word_c):
		count_w+=frequency_tri[word_a+word_b+word_c]
	return (count_w+1)/(count+data_length)

def unigram(sentence):
	words=copy_word(sentence)
	# print(words)
	p=frequency(words[0])
	for x in range(0,len(words)):
		p*=frequency(words[x])
	return p

def bigram(sentence):
	words=copy_word(sentence)
	# print(words)
	p=frequency(words[0])
	for x in range(len(words)-1):
		p*=calculate_condition_probability(words[x+1],words[x])
	return p

def trigram(sentence):
	words=copy_word(sentence)
	# print(words)
	if len(words)<3:
		print(words)
		print("长度不足")
		return -1
	p=frequency(words[0])
	p*=calculate_condition_probability(words[1],words[0])
	for x in range(len(words)-2):
		p*=calculate_condition_probability_3(words[x+2],words[x+1],words[x])
	return p
def get_perplexity(sentence):
	words=copy_word(sentence)
	print(words)
	p=log(frequency(words[0]))
	for x in range(len(words)-1):
		p+=log(calculate_condition_probability(words[x+1],words[x]))
	p=2**(-(p)/len(words))
	return p


init()


		
s1="喜欢我运动"
s2="怎么会对自己手下留情"
s3="京东举办了全球首届任务导向型多轮对话系统挑战赛"
print(get_perplexity(s3))


res=bigram(s3)>bigram(s2)
print()
print("*"*25)
if unigram(s3)>unigram(s2):
	print(f"unigram: {s3}是人话")
else:
	print(f"unigram: {s2}是人话")

if res:
	print(f" bigram: {s3}是人话")
else:
	print(f" bigram: {s2}是人话")

if trigram(s3)>trigram(s2):
	print(f"trigram: {s3}是人话")
else:
	print(f"trigram: {s2}是人话")
print()
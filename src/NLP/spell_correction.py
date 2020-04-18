# test.py
# spell correction.py
import time 
import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('../../res/big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N


def edits1(word):

    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]

    return set(deletes + transposes + replaces + inserts)
def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


# def correction(word): 
#     "Most probable spelling correction for word."
#     keneng_words=list(candidates(word))
#     res=[keneng_words[0],P(keneng_words[0])]
#     for x in keneng_words:
# 	    p=P(x)
# 	    if p>res[1]:
# 	    	res[0]=x
# 	    	res[1]=p
#     return res[0]
# print(correction('applaa'))

def correction(word): 
    return max(candidates(word), key=P)

words_all=words(open('../../res/mis_words.txt').read())
words=open('../../res/mis_words.txt').read()
rigth=[line.split(':')[0] for line in words.split('\n') if line !='']


start = time.clock()
r_count=0
count=0
r_words=[]
for word in words_all:
	res=correction(word)
	count+=1
	if word!=res:
		r_count+=1
		r_words.append(res)
	else:
		r_words.append(word)

# print(count-r_count,r_count)
# print(len(rigth))
df= time.clock()-start

erro=set(r_words)-set(rigth)

print(f"正确率 :{round((1-len(erro)/r_count)*100)}% \n纠错速度:{round(r_count/df)} 词/秒")

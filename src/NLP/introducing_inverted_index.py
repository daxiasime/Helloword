# introducing_inverted_index.py
import os
path="corpus/chinese"
print(os.listdir(path))
"""
[
 'science.yml', 'literature.yml', 'humor.yml', 'botprofile.yml', 
 'food.yml', 'conversations.yml', 'greetings.yml', 'ai.yml',
 'politics.yml', 'history.yml', 'gossip.yml', 'emotion.yml',
 'psychology.yml', 'trivia.yml', 'money.yml', 'movies.yml', 'sports.yml'

 ]

 [
 科学,文学,幽默,介绍自己,
 食物,对话,问候,ai,
 政治,历史,流言蜚语,情感,
 心理学,旅行,金钱,电影,运动.
 ]
"""

#分大方向.

def  first_filter(sentence):
	pass
	
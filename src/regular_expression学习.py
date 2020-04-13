import re
"""
Tips:

	#1 re.match(pattern, string, flags=0) 从字符串的开始开始匹配，如果不符合则返回None ，符合返回一个match对象。
		使用match.group()，可查看返回的信息

	#2 re.search(pattern, string, flags=0) 从字符串开始比较，只到字符串结束，只要匹配到就返回，如果不存在，返回None 。
		就像他的名字那样——搜索

	#3 re.findall(pattern,string) 选取所有合适的条目，如果用了括号，则只显示括号内部的
		如果不想只显示部分 可用(?:pattern)来代替（pattern）

	#4 re.sub(pattern, repl, string, count=0, flags=0)选取所有合适的条目使用指定字符串来代替
	    不用使用(?:pattern)代替括号
		repl 	替换的字符串，也可为一个函数。
		count 	模式匹配后替换的最大次数，默认 0 表示替换所有的匹配

	#5 re.split(pattern, string  [, maxsplit=0, flags=0])按照能够匹配的子串将字符串分割后返回列表
		要使用(?:pattern)代替括号，否则只能匹配括号内的部分。
		maxsplit 分隔次数，maxsplit=1 分隔一次，默认为 0，不限制次数

	正则表达式修饰符
		修饰符被指定为一个可选的标志。多个标志可以通过按位 OR(|) 它们来指定。
		re.I 	使匹配对大小写不敏感
		re.L 	做本地化识别（locale-aware）匹配
		re.M 	多行匹配，影响 ^ 和 $
		re.S 	使 . 匹配包括换行在内的所有字符
		re.U 	根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
		re.X 	该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。

"""
s=" industries industry industry industries industriea industrie4 "
# pattern=re.compile('industr(?:y|ies)',flags=re.M)

# # res=re.match(pattern,s)
# # res=re.search(pattern,s)
# res=re.findall(pattern,s)
# # res=re.sub(pattern,"in*****",s)
# # res=re.split(pattern,s)
# if res==None:
# 	print(None)
# else:
# 	print(res)
pattern1=re.compile('industr(?:y|ies)',flags=re.M)
pattern2=re.compile('industr(y|ies)',flags=re.M)
res1=re.findall(pattern1,s)
res2=re.findall(pattern2,s)
print(res1)
print(res2)



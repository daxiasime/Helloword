import re
s=open('../res/email.txt','r').read()
pattern=re.compile('[0-9A-Za-z_]+([-+.]\w+)*@[0-9a-z]+\.[a-z.]+')
res=pattern.finditer(s)

c=[m.group(0) for m in res ]

print('\n'.join(c))
'''
邮箱查询
主演上映信息
data=re.findall('title="(.*?)" c.*?(主演.*?)\n.*?(上映时间.*?)<.*?nteger">([0-9]\.).*?on">([0-9])</i>',s,re.S)
for x in data:
	print(f"{x[0]}\n{x[1]}  \n{x[2]}  \n评分：{x[3]+x[4]}") 
	print("分割线".center(20,'-'))
'''

# pattern = re.compile(u'src="(http[a-z]?:)?.*?\.(jpg|png)')
# print(pattern.search(s))
# res=list(set(res))
# print('\n\n'.join(res))

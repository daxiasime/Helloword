# 解析邮箱.py
import re
s=open('../res/email.txt','r').read()

"""
    Email地址：^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$

Tips
     1#  \w 和[a-zA-Z_] 不相同，\w 可以匹配汉字。
     2#  finditer(str) 返回一个迭代器。

"""
email_pattern=re.compile('[0-9A-Za-z_-]*@[0-9a-zA-Z]+\.[A-Za-z.]*')

email_res=email_pattern.finditer(s)

emails=[m.group(0) for m in email_res ]
emails=list(set(emails))
print('\n'.join(emails))
print(f"共计{len(emails)}条记录")


# 解析qq
# qq_pattern=re.compile('[1-9][0-9]{7,12}')
# qq_res=qq_pattern.finditer(s)
# qq=[m.group(0) for m in qq_res ]
# qq=list(set(qq))
# print('\n'.join(qq))
# print(f"共计{len(qq)}条记录")
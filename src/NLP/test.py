# test.py
import re

# p=re.compile('class="content">\n(.*? *  )</div>',re.S)
# print(re.findall(p,text))
import jieba
import pandas as pd

#任意的多组列表
a = None
b = None    

#字典中的key值即为csv中列名
dataframe = pd.DataFrame({'a_name':a,'b_name':b})

#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe.to_csv("test.csv",index=False,sep=',')
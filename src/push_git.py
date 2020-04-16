# push_git.py
import os
import datetime
log="submit on "+str(datetime.datetime.now()).split('.')[0]
os.chdir('../')
os.system("git add src ")
os.system("git add res ")
os.system(f"git commit -m '{log}'")
os.system("git push ds master")
print(log)
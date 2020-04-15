# threading_lock.py 
import json
import  time
import  os
import threading
from multiprocessing import  Lock



class buy_ticket(threading.Thread):
	def __init__(self,name,lock):
		threading.Thread.__init__(self)
		self.name=name
		self.lock=lock
	def run(self):
		self.__buy_ticket()

	def __buy_ticket(self):
		self.lock.acquire()#枷锁
		time.sleep(0.5)
		ticket=int(open('ticket','r').read())
		if ticket>0:
			ticket-=1
			with open('ticket','w') as f:
				f.write(str(ticket))
			print(f'{self.name} ,买到了票！')
		elif ticket==0:
			print(f'{self.name} ,票已售空！')
		self.lock.release()#解锁

		

if __name__=='__main__':
    lock=Lock()  
    for i in range(5):
        p=buy_ticket(f'{i}号用户',lock)
        p.start()

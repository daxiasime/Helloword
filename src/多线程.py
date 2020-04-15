import time
import threading
# 使用 threading 模块创建线程
import queue
#优先级队列模块
#线程优先级队列(Queue)
exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        # print ("开启线程：" + self.name)
        process_data(self.threadID,self.name, self.q)
        # print ("退出线程：" + self.name)


def process_data(id,threadName, q):
    while not exitFlag:
        id += 1
        if id >= 4:
            if q.empty():
                return 
            data = q.get()
            # print ("%s processing %s" % (threadName, data))
        time.sleep(1)
def process_bar(current,total):
    index=round((1-current/total)*100,1)
    s1=' '*round((100-index)/2)
    s2='▊'*round(index/2)
    print(f"|{s2+s1}|{index}%\r",end="")

        
threadList = ["Thread-1", "Thread-2"]
nameList = [str(i) for i in range(100)]
workQueue = queue.Queue(100)
threads = []
threadID = 1
# 填充队列
for work in nameList:
    workQueue.put(work)
# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
# 等待队列清空
while not workQueue.empty():
    time.sleep(0.2)
    process_bar(workQueue.qsize(),len(nameList))
# 通知线程是时候退出
exitFlag = 1
# 等待所有线程完成
for t in threads:
    t.join()
print ("\n退出主线程")

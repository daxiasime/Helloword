import queue
q=queue.Queue(10)
for i in range(10):
	q.put(i)
q.get()
q.task_done()
print(q.qsize())
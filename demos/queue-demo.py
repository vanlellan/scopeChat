
import Queue as qu
import thread


def worker(aQ, ID_in_list):
	while ID_in_list[0] >= 0:
		item = aQ.get()
		print "Worker"+str(ID_in_list[0])+" Print: ", item
		q.task_done()


workerDict = {}
q = qu.Queue()



while True:
	command = raw_input("> ")

	if command in ['exit','quit','q']:	#break main loop
		for key in workerDict:
			workerDict[key][0] = -1
		break

	elif command == 'add':
		newList = [len(workerDict),]
		t = thread.start_new_thread(worker,(q,newList))
		workerDict[t] = newList
		print len(workerDict), "total workers."

	elif command == 'run':
		q.join()	#not required for workers to work! only use if you need this thread to wait until queue is empty

	elif command == '1000':
		for i in range(1000):
			q.put(str(i))

	else:
		q.put(command)

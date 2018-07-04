import thread
import time

def counter(uniList):	#argument is a list with one element, which will be used as a counter (it's a list to get pass-by-reference behavior)
	while True:
		if uniList[0]==-1:	#if counter has been set to zero break loop to kill this thread
			break
		else:
			uniList[0] += 1	#increment counter
			time.sleep(1)	#sleep 1 seconds

threadDict = {}	#dictionary to keep track of thread IDs and associated counters

while True:
	command = raw_input("> ")	#blocking input on main thread, wait for user command
	if command in ['exit','quit','q']:	#kill all threads and break main loop
		for key in threadDict:
			threadDict[key][0] = -1
		break
	if command == 'new':	#start new thread with a counter initialized to zero
		newList = [0,]	#initialize counter-in-a-list to zero
		t = thread.start_new_thread(counter,(newList,))	#start new counter function in new thread, passing it the new counter-in-a-list
		threadDict[t] = newList	#add thread and associated counter-in-a-list to dictionary
	if command == 'print':	#print all counters
		for key in threadDict:
			print "key=", key, "    count=",threadDict[key][0]



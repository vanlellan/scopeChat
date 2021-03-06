import socket
import thread
import Queue as qu

def clientListen(aConnection, aQ):
    while True:
        buf = aConnection.recv(64)
        if buf == '':	#kill thread if empty buffer is sent (usually due to broken connection)
            print "Client left."
            break
        aQ.put(buf)

def clientsBroadcast(aDict, aQ, aKillSwitch):
    while True:
        message = aQ.get()
        aKillSwitch[1] += 1
        for aC in aDict:
            aDict[aC].send(message)
        aKillSwitch[1] -= 1
        aQ.task_done()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 5406))
serversocket.listen(5) # become a server socket, maximum 5 connections

clientDict = {}
killSwitch = [False,0]	#first element is killswitch (now unused), second is pause (make this a "control dictionary" or "control object")
q = qu.Queue()

broadcaster = thread.start_new_thread(clientsBroadcast,(clientDict, q, killSwitch))

print "Ready \n"

while True:
    connection, address = serversocket.accept()
    newClient = thread.start_new_thread(clientListen,(connection, q))
    print "Got new client! address = ", address
    while killSwitch[1] != 0:
        print "waiting for unpause..."
        pass
    clientDict[newClient] = connection

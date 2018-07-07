import socket
import thread
import sys

def clientOut(clientsocket):
	while True:
		message = raw_input("> ")
		clientsocket.send(message)
		if message in ('exit','kill','quit'):
			break
	clientsocket.close()

def runClient():
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsocket.connect(('localhost', 8089))
	#clientsocket.connect(('192.168.1.109', 8089))

	to = thread.start_new_thread(clientOut,(clientsocket,))

	while True:
		inbound = clientsocket.recv(1024)
		if len(inbound) > 0:
			print inbound,'\n'
		if inbound in ('exit','kill','quit'):
			break

	clientsocket.close()

def runServer():
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind(('localhost', 8089))
	serversocket.listen(5) # become a server socket, maximum 5 connections

	print "Ready \n"

	connection, address = serversocket.accept()
	while True:
		buf = connection.recv(64)
		if len(buf) > 0:
			print buf
			connection.send(buf)
		if buf == "kill":
			break

mode = sys.argv[1]

if mode == "server":
	print "Starting Server..."
	runServer()
elif mode == "client":
	print "Starting Client..."
	runClient()
else:
	print "First arg must be \"client\" or \"server\""









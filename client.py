import socket
import thread

def incoming(clientsocket):
	while True:
		inbound = clientsocket.recv(1024)
		if len(inbound) > 0:
			print inbound,'\n'

def outgoing(clientsocket):
	while True:
		message = raw_input("> ")
		clientsocket.send(message)
		if message in ('exit','kill','quit'):
			break
	clientsocket.close()

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))

ti = thread.start_new_thread(incoming,(clientsocket,))
to = thread.start_new_thread(outgoing,(clientsocket,))

while True:
	pass

clientsocket.close()

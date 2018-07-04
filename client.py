import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientsocket.connect(('localhost', 8089))
clientsocket.connect(('192.168.1.109', 8089))


while True:
	message = raw_input("Type message: ")
	clientsocket.send(message)
	reply = clientsocket.recv(1024)
	if len(reply) > 0:
		print reply
	if message in ('exit','kill','quit'):
		break

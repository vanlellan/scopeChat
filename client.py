import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))


while True:
	message = raw_input("Type message: ")
	if message == 'exit':
		break
	clientsocket.send(message)
	reply = clientsocket.recv(1024)
	if len(reply) > 0:
		print reply

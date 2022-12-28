from socket import *
from threading import *
from pathlib import *

serverName ='127.0.0.1'
serverPort = 1234
clientPort = 5678
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)

serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print ("proxy ready")

def recv1(connectionSocket): 
	while True:
		req = connectionSocket.recv(4096).decode('utf-8')
		if not req:
			return req
		if req.find('\n'):
			if((req.split('\n',1) [0] [0:4]) != "HTTP"):
				return req
			else:
				clientSocket.sendall(req.encode('utf-8'))
def recv2(clientSocket):
	while True:
		req = clientSocket.recv(4096).decode('utf-8')
		if not req:
			return req
		if req.find('\n'):
			if((req.split('\n',1) [0] [0:4]) != "HTTP"):
				return req
			else:
				connectionSocket.sendall(req.encode('utf-8'))

def handle_client(connectionSocket):
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
	clientSocket.connect((serverName, clientPort))
	request = recv1(connectionSocket) 
	filename = Path(request.split("\n",1)[0].split(" ")[1].lstrip("/"))
	print("the file", filename , "is requested \n")
	if not filename.is_file():
		print("there is no file with this name on proxy")
		clientSocket.sendall(request.encode('utf-8'))
		serv_req = recv2(clientSocket)
#then
		connectionSocket.sendall(serv_req.encode('utf-8'))
		filemodified = open(filename, "w")
		filemodified.write(serv_req)
		print ("---after asking the main server---")
		print("now the file is found and is retrieved from the server")
		filemodified.close()
		clientSocket.close()
		connectionSocket.close()
	else:
		connectionSocket.sendall(b"HTTP/1.1 200 OK\n")
		with open(filename ,"br") as f:
			connectionSocket.sendall(f.read())
		clientSocket.close()
		connectionSocket.close()

while True:
	connectionSocket, address = serverSocket.accept()
	Thread(target = handle_client, args = (connectionSocket,)).start()

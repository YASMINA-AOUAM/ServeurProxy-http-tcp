from socket import *
from pathlib import *

serverPort = 5678
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('server ready')

def recv_until(connectionSocket):
	file_asked = ""
	while True:
		req = connectionSocket.recv(4096).decode('utf-8')
		if not req and len(file_asked)!=0:
			return file_asked
		file_asked += req
		if req.find('\n'):
			return file_asked.split('\n',1)[0]

def handle_client(connectionSocket):
	file_asked = recv_until(connectionSocket)
	if len(file_asked)!=0 :
		filename = Path(file_asked.split(" ")[1].lstrip("/"))
		print("the file", filename, "is requested")
		if not filename.is_file():
			print("unfortunately not found")
			connectionSocket.sendall(b"HTTP/1.1 404 Not Found\nServer: Python HTTP Server\nConnection: close\r\n\r\n")
		else:
			print("obviously found and will be sent")
			connectionSocket.sendall(b"HTTP/1.1 200 OK\nServer: Python HTTP Server\nConnection: close\r\n\r\n")
			with open(filename,"br") as f:
				connectionSocket.sendall(f.read())
				connectionSocket.close()
while True:
	connectionSocket, address = serverSocket.accept()
	handle_client(connectionSocket)


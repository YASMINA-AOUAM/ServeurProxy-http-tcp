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
	request ="" 
	while True:
		req = connectionSocket.recv(4096).decode('utf-8')
		if not req:
			return request
		request += req
		if req.find('\n'):
			if((req.split('\n',1)[0][0:3]) == "GET"):
				return req
			else:
				if((req.split('\n',1)[0][0:4])!="HTTP"):
					return request
				else: 
					clientSocket.sendall(req.encode('utf-8'))
def recv2(clientSocket):
	serv_req =""
	while True:
		req = clientSocket.recv(4096).decode('utf-8')
		if not req:
			return serv_req
		serv_req +=req
		if req.find('\n'):
			if((req.split('\n',1) [0] [0:3]) == "GET"):
				return req
			else:
				if((req.split('\n',1)[0][0:4])!= "HTTP"):
					return serv_req
				else:
					connectionSocket.sendall(req.encode('utf-8'))

def handle_client(connectionSocket):
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
	clientSocket.connect((serverName, clientPort))
	request = recv1(connectionSocket)
	with open ('logfile.txt', 'a') as log:
		log.write(request + "\n")
	clientSocket.sendall(request.encode('utf-8'))
	serv_req= recv2(clientSocket)
	line = serv_req.split("\r\n")
	word = []
	for i in line:
		word += str(i).split("\n")
	size = []
	for i in word:
		size += str(i).split(" ")
	j = 0
	for i in range(len(size)):
		if size[i] == "Content-Length:":
			j = i + log
	if j:
		with open('logfile.txt', 'a') as log:
			log.write("\n" + serv_req + "\n" + "file length"+  size[j])
	else:
		with open('logfile.txt', 'a') as log:
			log.write(serv_req + "\n" + "unkown length" + "\n")
	connectionSocket.sendall(serv_req.encode('utf-8'))
	clientSocket.close()
	connectionSocket.close()
 
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

from socket import *
import time as t
from threading import *

serverName ='127.0.0.1'
serverPort = 5678

serverSocket = socket(AF_INET, SOCK_STREAM) #creation d'une socket du server
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
serverSocket.bind ((('',serverPort))) # ecoute sur le port du serveur
serverSocket.listen(15)

print ('server ready')

def handle_client(connectionSocket):
	request = connectionSocket.recv(2048).decode('utf-8') # reception de la>
	print (  request)
	response = " I have received your message successfully"
	t.sleep(1)
	connectionSocket.send(response.encode('utf-8'))
	#print ('the message I send back to the client :', response)

while True:
	connectionSocket, address = serverSocket.accept() #le serveur accepte sur le port 5678
	Thread(target = handle_client, args=(connectionSocket,)).start()

